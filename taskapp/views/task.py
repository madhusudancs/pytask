from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect

from pytask.taskapp.models import User, Task, Comment, Claim, Request, Notification
from pytask.taskapp.utilities.task import getTask
from pytask.taskapp.forms.task import TaskCreateForm, AddMentorForm, AddTaskForm, ChoiceForm, AssignCreditForm, RemoveUserForm, EditTaskForm
from pytask.taskapp.events.task import createTask, reqMentor, publishTask, addSubTask, addDep, addClaim, assignTask, updateTask, removeTask, removeUser, assignCredits, completeTask, closeTask, addMentor
from pytask.taskapp.views.user import show_msg
from pytask.taskapp.utilities.user import get_user

## everywhere if there is no task, django should display 500 message.. but take care of that in sensitive views like add mentor and all
## do not create su user thro syncdb

def browse_tasks(request):
    """ display all the tasks """
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task_list = Task.objects.exclude(status="UP").exclude(status="DL").order_by('published_datetime').reverse()
    
    context = {'user':user,
               'task_list':task_list,
               }
    return render_to_response('task/browse.html', context)

def publish_task(request, tid):
    """ check if user is the mentor and also if the task status is UP.
    """

    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)

    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False

    if user == task.created_by:
        context = {
            'user':user,
        }
        if task.status == "UP":
            if request.method == "POST":
                publishTask(task)
                return show_msg(user, "The task has been published", task_url, "view the task")
            else:
                return render_to_response('task/publish.html', context)
        else:
            return show_msg(user, "The task is already published", task_url, "view the task")
    else:
        return show_msg(user, "You are not authorised to do this", '/task/browse/', "browse tasks")

def view_task(request, tid):
    """ get the task depending on its tid and display accordingly if it is a get.
    check for authentication and add a comment if it is a post request.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)

    if task.status == "DL":
        return show_msg(user, 'This task no longer exists', '/task/browse/','browse the tasks')
    comments = task.comment_set.filter(is_deleted=False).order_by('creation_datetime')
    mentors = task.mentors.all()

    deps, subs = task.deps, task.subs
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False
    context = {'user':user,
               'task':task,
               'comments':comments,
               'mentors':mentors,
               'subs':subs,
               'deps':deps,
               'is_guest':is_guest,
               'is_mentor':is_mentor,
              }

    claimed_users = task.claimed_users.all()

    context['task_viewable'] = True if ( task.status != "UP" ) or is_mentor else False

    context['can_publish'] = True if task.status == "UP" and user == task.created_by else False
    context['can_edit'] = True if ( not claimed_users ) and task.status in ["UP", "LO", "OP"] and is_mentor else False
    context['can_close'] = True if task.status not in ["UP", "CD", "CM"] and is_mentor else False

    context['can_mod_mentors'] = True if task.status in ["UP", "OP", "LO", "WR"] and is_mentor else False
    context['can_mod_tasks'] = True if task.status in ["UP", "OP", "LO"] and is_mentor else False

    context['can_assign_credits'] = True if task.status in ["OP", "WR"] and is_mentor else False
    context['task_claimable'] = True if task.status in ["OP", "WR"] and not is_guest else False

    if task.status == "CD":
        context['closing_notification'] =  Notification.objects.filter(task=task,role="CD")[0]
    elif task.status == "CM":
        context['completed_notification'] =  Notifications.objects.filter(task=task,role="CM")[0]
    elif task.status == "WR":
        context['assigned_users'] = task.assigned_users.all()
   
    if request.method == 'POST':
        if not is_guest:
            data = request.POST["data"]
            new_comment = Comment(task=task, data=data, created_by=user, creation_datetime=datetime.now())
            new_comment.save()
            return redirect(task_url)
        else:
            errors.append("You must be logged in to post a comment")
            return render_to_response('task/view.html', context)
    else:
        return render_to_response('task/view.html', context)
        
def create_task(request):
    """ check for rights and create a task if applicable.
    if user cannot create a task, redirect to homepage.
    """
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    is_guest = True if not user.is_authenticated() else False
    
    if not is_guest:
        user_profile = user.get_profile()
        can_create_task = False if user_profile.rights == "CT" else True
        if can_create_task:
            if request.method == "POST":
                form = TaskCreateForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    title = data['title']
                    desc = data['desc']
                    credits = data['credits']
                    #publish = data['publish'] # just in case if we have to show the option
                    task = createTask(title,desc,user,credits)
                    
                    if not task:
                        error_msg = "Another task with the same title exists"
                        return render_to_response('task/create.html',{'user':user, 'form':form, 'error_msg':error_msg})
                    
                    addMentor(task, user)
                    updateTask(task,tags_field=data['tags_field'])
                    # if publish: publishTask(task)    
                    task_url = '/task/view/tid=%s'%task.id
                    return redirect(task_url)
                else:
                    return render_to_response('task/create.html',{'user':user, 'form':form})
            else:
                form = TaskCreateForm()
                return render_to_response('task/create.html',{'form':form})
        else:
            return show_msg(user, 'You are not authorised to create a task.')
    else:
        return show_msg(user, 'You are not authorised to create a task.')
        
def add_mentor(request, tid):
    """ check if the current user has the rights to edit the task and add him.
    if user is not authenticated, redirect him to concerned page. """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)
    errors = []
    
    is_guest = True if not user.is_authenticated() else False
    
    if (not is_guest) and user in task.mentors.all():

        pending_requests = Request.objects.filter(is_replied=False,is_valid=True,role="MT",task=task).order_by('creation_date').reverse()
        user_pending_requests = pending_requests.filter(sent_by=user)

        ## now iam going for a brute force method
        user_list = list(User.objects.filter(is_active=True))
        for mentor in task.mentors.all():
            user_list.remove(mentor)
            
        for a_user in task.claimed_users.all():
            user_list.remove(a_user)

        for a_user in task.assigned_users.all():
            user_list.remove(a_user)

        for req in user_pending_requests:
            user_list.remove(req.sent_to.all()[0])
            
        non_mentors = ((_.id, _.username) for _ in user_list)
        non_mentor_ids = [ str(a_user.id) for a_user in user_list ]
        ## code till must be made elegant and not brute force like above

        form = AddMentorForm(non_mentors)

        context = {
            'user':user,
            'task':task,
            'pending_requests':pending_requests,
            'form':form,
        }

        if request.method == "POST":
            data = request.POST
            uid = data.get('mentor', None)
            if uid in non_mentor_ids:
                new_mentor = User.objects.get(id=int(uid))
                reqMentor(task, new_mentor, user)
                return redirect('/task/addmentor/tid=%s'%task.id)
            else:
                ## bogus post request
                raise Http404
        else:
            return render_to_response('task/addmentor.html', context)
    else:
        return show_msg(user, 'You are not authorised to add mentors for this task', task_url, 'view the task')
    
def add_tasks(request, tid):
    """ first display tasks which can be subtasks for the task and do the rest.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)

    deps, subs = task.deps, task.subs
    is_plain = False if deps or subs else True

    ## again a brute force method
    valid_tasks = []
    for a_task in Task.objects.all():
        if not ( a_task in deps or a_task in subs or a_task.status=="CD" or a_task==task ):
            valid_tasks.append(a_task)

    task_choices = [ (_.id,_.title) for _ in valid_tasks ]
    errors = []
    
    is_guest = True if not user.is_authenticated() else False
    
    if (not is_guest) and user in task.mentors.all():
        if task.status in ["UP", "OP", "LO"]:
            form = AddTaskForm(task_choices, is_plain)
            if request.method == "POST":
                ## first decide if adding subs and deps can be in same page
                ## only exclude tasks with status deleted
                data = request.POST
                if is_plain and not data.get('type', None): errors.append('Please choose which type of task(s) do you want to add.')
                if not data.get('task', None): errors.append('Please choose a one task')

                if not errors:
                    if is_plain:
                        update_method = addDep if data['type'] == "D" else addSubTask
                    elif deps:
                        update_method = addDep
                    elif subs:
                        update_method = addSubTask
                    else:
                        print "Screw you"

                    ## we might iterate over a task list later on
                    task_id = data['task']
                    sub_or_dep = getTask(task_id)
                    update_method(task, sub_or_dep)

                    return redirect(task_url)
                else:
                    return render_to_response('task/addtask.html', {'user':user, 'form':form, 'errors':errors})
            else:
                return render_to_response('task/addtask.html', {'user':user, 'form':form, 'errors':errors})
        else:
            errors = ["The task cannot be added subtasks or dependencies in this state"]
#            return render_to_response('task/add.html', {'form':form, 'errors':errors})
            return show_msg(user, 'The task cannot be added subtasks or dependencies now', task_url, 'view the task')
    else:
        return show_msg(user, 'You are not authorised to add subtasks or dependencies for this task', task_url, 'view the task')
    
def remove_task(request, tid):
    """ display a list of tasks and remove the selectes ones.
    """

    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)

    is_guest = True if not user.is_authenticated() else False
    if (not is_guest) and user in task.mentors.all():

        if task.status in ["UP", "LO", "OP"]:
            
            deps, subs = task.deps, task.subs
            task_list = deps if task.sub_type == "D" else subs

            if task_list:
                choices = [(_.id,_.title) for _ in task_list ]
                form = ChoiceForm(choices)

                errors = []
                
                context = {
                    'user':user,
                    'task':task,
                    'form':form,
                }

                if request.method == "POST":
                    data = request.POST
                    if not data.get('choice', None):
                        errors.append("Please choose a task to remove.")
                        context['errors'] = errors
                    if not errors:
                        tid = data['choice']
                        sub_task = getTask(tid)
                        removeTask(task, sub_task)
                        return redirect(task_url)
                    else:
                        return render_to_response('task/removetask.html', context)
                else:
                    return render_to_response('task/removetask.html', context)
            else:
                return show_msg(user, "The task has no subtasks/dependencies to be removed", task_url, "view the task")
        else:
            return show_msg(user, "subtasks/dependencies cannot be removed at this stage", task_url, "view the task")
    else:
        return show_msg(user, "You are not authorised to do this", task_url, "view the task")

def claim_task(request, tid):
    """ display a list of claims for get and display submit only if claimable """

    ## create claims model and create a new database with required tables for it
    ## see if that "one to n" or "n to one" relationship has a special field
    
    task_url = "/task/view/tid=%s"%tid
    claim_url = "/task/claim/tid=%s"%tid
    
    errors = []
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)
    claims = Claim.objects.filter(task=task)

    mentors = task.mentors.all()
    claimed_users = task.claimed_users.all()
    assigned_users = task.assigned_users.all()
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in mentors else False

    task_claimable = True if task.status in ["OP", "WR"] else False
    user_can_claim = True if  task_claimable and not ( is_guest or is_mentor ) and ( user not in claimed_users ) and ( user not in assigned_users )  else False
    task_claimed = True if claimed_users else False
    
    context = {'user':user,
               'is_mentor':is_mentor,
               'task':task,
               'claims':claims,
               'user_can_claim':user_can_claim,
               'task_claimable':task_claimable,
               'task_claimed':task_claimed,
               'errors':errors}
    
    if not is_guest:
        if request.method == "POST":
            claim_proposal = request.POST['message']
            if claim_proposal:
                addClaim(task, claim_proposal, user)
                return redirect(claim_url)
            else:
                errors.append('Please fill up proposal in the field below')
                return render_to_response('task/claim.html', context)
        else:
            return render_to_response('task/claim.html', context)
    else:
        return show_msg(user, 'You are not logged in to view claims for this task', task_url, 'view the task')
    
def rem_user(request, tid):
    """ show a list of working users and ask for a message/reason for removing user.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False

    if (not is_guest) and is_mentor:

        assigned_users = task.assigned_users.all()
        choices = [ (_.id,_.username) for _ in assigned_users ]
        context = {
            'user':user,
            'task':task,
        }
        
        if task.status in ["WR"]:
            if assigned_users:
                form = RemoveUserForm(choices)
                context['form'] = form
                if request.method == "POST":
                    data = request.POST
                    form = RemoveUserForm(choices, data)
                    if form.is_valid():
                        data = form.cleaned_data
                        uid = data['user']
                        reason = data['reason']
                        rem_user = User.objects.get(id=uid)
                        removeUser(task, rem_user, user, reason)
                        return redirect(task_url)
                    else:
                        context['form'] = form
                        return render_to_response('task/remove_user.html', context)
                else:
                    return render_to_response('task/remove_user.html',context)
            else:
                return show_msg(user, "There is no one working on this task to be kicked off", task_url, "view the task")
        else:
            return show_msg(user, "This is not the stage to remove users", task_url, "view the task")
    else:
        return show_msg(user, "You are not authorised to do this", task_url, "view the task")

def assign_task(request, tid):
    """ first get the status of the task and then assign it to one of claimed users
    generate list of claimed users by passing it as an argument to a function.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False

    claimed_users = task.claimed_users.all()
    assigned_users = task.assigned_users.all()

    task_claimed = True if claimed_users else False
    
    if (not is_guest) and is_mentor:
        if task.status in ["OP", "WR"]:
            if task_claimed:
                user_list = ((user.id,user.username) for user in claimed_users)
                form = ChoiceForm(user_list)
        
                if request.method == "POST":
                    uid = request.POST['choice']
                    assigned_user = User.objects.get(id=uid)
                    assignTask(task, assigned_user, user)
                    return redirect(task_url)
                else:
                    return render_to_response('task/assign.html',{'user':user, 'task':task,'form':form})
            elif assigned_users:
                return show_msg(user, 'When the no of users you need for the task is more than the no of users willing to do the task, I\'d say please re consider the task :P',task_url, 'view the task')
            else:
                return show_msg(user, 'Wait for ppl to claim dude... slow and steady wins the race :)', task_url, 'view the task')
        else: 
            return show_msg(user, "The task cannot be assigned to users at this stage", task_url, 'view the task')
    else:
        return show_msg(user, 'You are not authorised to perform this action', task_url, 'view the task')

def assign_credits(request, tid):
    """ Check if the user is a mentor and credits can be assigned.
    Then display all the approved credits.
    Then see if mentor can assign credits to users also or only mentors.
    Then put up a form for mentor to assign credits accordingly.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)

    ## the moment we see that user had requested credits, it means he had worked and hence we change the status to WR
    ## we have to discuss on this since, credits may also be given to mentor
    task.status = "WR"
    task.save()

    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if (not is_guest) and user in task.mentors.all() else False

    if is_mentor:
        if task.status in ["OP", "WR"]:
            choices = [(_.id,_.username) for _ in task.mentors.all()]
            if task.status == "WR":
                choices.extend([(_.id, _.username) for _  in task.assigned_users.all() ])
            prev_credits = task.request_task.filter(role="PY",is_valid=True,is_replied=True,reply=True).count()
            credit_requests = task.request_task.filter(role="PY",is_valid=True).order_by('creation_date').reverse()
            form = AssignCreditForm(choices)

            context = {
                'user':user,
                'task':task,
                'prev_credits':prev_credits,
                'credit_requests':credit_requests,
                'form':form,
            }

            if request.method == "POST":
                data = request.POST
                form = AssignCreditForm(choices, data)
                if form.is_valid():
                    data = form.cleaned_data
                    uid = data['user']
                    points = data['pynts']
                    given_to = User.objects.get(id=uid)
                    assignCredits(task=task, given_by=user, given_to=given_to, points=points)
                    return redirect('/task/assigncredits/tid=%s'%task.id)
                else:
                    context['form'] = form
                    return render_to_response('task/assigncredits.html', context)
            else:
                return render_to_response('task/assigncredits.html', context)
        else:
            return show_msg(user, "Credits cannot be assigned at this stage", task_url, "view the task")
    else:
        return show_msg(user, "You are not authorised to perform this action", task_url, "view the task")

def edit_task(request, tid):
    """ see what are the attributes that can be edited depending on the current status
    and then give the user fields accordingly.
    """
    
    task = Task.objects.get(id=tid)
    task_url = "/task/view/tid=%s"%tid
    user = get_user(request.user) if request.user.is_authenticated() else request.user

    is_mentor = True if user in task.mentors.all() else False
    can_edit = True if is_mentor and task.status == "UP" else False

    if can_edit:
        form = EditTaskForm(task)
        if request.method=="POST":
            data = request.POST
            form = EditTaskForm(task, data)
            if form.is_valid():
                data = form.cleaned_data
                title = data['title']
                try:
                    prev_task = Task.objects.exclude(status="DL").get(title=title)
                    if prev_task != task:
                        error_msg = "Another task exists with the same title"
                        return render_to_response('task/edittask.html',{'user':user, 'form':form, 'error_msg':error_msg})
                except Task.DoesNotExist:
                    pass
                task.title = title
                task.desc = data['desc']
                task.tags_field = data['tags_field']
                task.credits = data['credits']
                task.save()
                return redirect(task_url)
            else:
                return render_to_response('task/edittask.html',{'user':user, 'form':form})
        else:
            return render_to_response('task/edittask.html',{'user':user, 'form':form})
    else:
        return show_msg(user, "You cannot edit the task at this stage", task_url, "view the task")

def complete_task(request, tid):
    """ call the event called complete task.
    and also pass it the current user to know who marked it as complete. 
    """

    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False

    claimed_users = task.claimed_users.all()
    assigned_users = task.assigned_users.all()

    assign_credits_url = '/task/assigncredits/tid=%s'%task.id
    task_assigned_credits = task.credit_set.all()


    if is_mentor:
        if task.status in ["OP", "WR"]:

            context = {
                'user':user,
                'task':task,
            }

            if task_assigned_credits:
                if request.method=="POST":
                    completeTask(task, user)
                    return redirect(task_url)
                else:
                    return render_to_response('task/complete.html', context)
            else:
                return show_msg(user, "Nobody has been credited for doing this task.", assign_credits_url, "assign credits")
        else:
            return show_msg(user, "The task cannot be marked as completed at this stage", task_url, "view the task")
    else:
        return show_msg(user, "You are not authorised to do this", task_url, "view the task")

def close_task(request, tid):
    """ task can be closed only if task is published.
    call the event close task if everything is fine.
    """

    task_url = "/task/view/tid=%s"%tid
    
    user = get_user(request.user) if request.user.is_authenticated() else request.user
    task = getTask(tid)
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False

    if is_mentor:

        context = {
            'user':user,
            'task':task,
        }

        if not task.status in ["UP", "CD", "DL", "CM"]:
            if request.method == "POST":
                data = request.POST
                if not data.get("reason", None):
                    context["error"] = "Please enter a reason for closing the task"
                    return render_to_response('task/close.html', context)
                else:
                    closeTask(task, user, data['reason'])
                    return show_msg(user, "The task has been closed.", task_url, "view the task.")
            else:
                return render_to_response('task/close.html', context)
        else:
            return show_msg(user, "The task is either already closed or cannot be closed at this stage", task_url, "view the task")
    else:
        return show_msg(user, "You are not authorised to do this", task_url, "view the task")

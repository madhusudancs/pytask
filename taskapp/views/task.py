from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from pytask.taskapp.models import User, Task, Comment, Claim
from pytask.taskapp.forms.task import TaskCreateForm, AddMentorForm, AssignTaskForm
from pytask.taskapp.events.task import createTask, addMentor, publishTask, addSubTask, addClaim, assignTask
from pytask.taskapp.views.user import show_msg

## everywhere if there is no task, django should display 500 message.. but take care of that in sensitive views like add mentor and all
## do not create su user thro syncdb

def browse_tasks(request):
    """ display all the tasks """
    
    user = request.user
    task_list = Task.objects.order_by('id').reverse()
    
    context = {'user':user,
               'task_list':task_list,
               }
    return render_to_response('task/browse.html', context)

def view_task(request, tid):
    """ get the task depending on its tid and display accordingly if it is a get.
    check for authentication and add a comment if it is a post request.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = request.user
    task = Task.objects.get(id=tid)
    comments = Comment.objects.filter(task=task)
    mentors = task.mentors.all()
    errors = []
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False
    
    task_claimable = True if task.status in ["OP", "RE"] else False
    
    context = {'user':user,
               'task':task,
               'comments':comments,
               'mentors':mentors,
               'is_guest':is_guest,
               'is_mentor':is_mentor,
               'errors':errors,
               }
               
    if task.status == "AS":
        context['assigned_user'] = task.assigned_users.all()[0]
    
    if request.method == 'POST':
        if not is_guest:
            data = request.POST["data"]
            task = Task.objects.get(id=tid)
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
    
    user = request.user
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
                    publish = data['publish']
                    task = createTask(title,desc,user,credits)
                    
                    if not task:
                        error_msg = "Another task with the same title exists"
                        return render_to_response('task/create.html',{'form':form, 'error_msg':error_msg})
                    
                    addMentor(task, user)
                    if publish: publishTask(task)    
                    task_url = '/task/view/tid=%s'%task.id
                    return redirect(task_url)
                else:
                    return render_to_response('task/create.html',{'form':form})
            else:
                form = TaskCreateForm()
                return render_to_response('task/create.html',{'form':form})
        else:
            return show_msg('You are not authorised to create a task.')
    else:
        return show_msg('You are not authorised to create a task.')
        
def add_mentor(request, tid):
    """ check if the current user has the rights to edit the task and add him.
    if user is not authenticated, redirect him to concerned page. """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = request.user
    task = Task.objects.get(id=tid)
    errors = []
    
    is_guest = True if not user.is_authenticated() else False
    
    if (not is_guest) and user in task.mentors.all():
        
        ## now iam going for a brute force method
        user_list = list(User.objects.all())
        for mentor in task.mentors.all():
            user_list.remove(mentor)
            
        for a_user in task.claimed_users.all():
            user_list.remove(a_user)
            
        non_mentors = ((_.id,_.username) for _ in user_list)
        ## code till must be made elegant and not brute force like above
        
        form = AddMentorForm(non_mentors)
        if request.method == "POST":
            uid = request.POST['mentor']
            new_mentor = User.objects.get(id=uid)
            addMentor(task, new_mentor)
            return redirect(task_url)
        else:
            return render_to_response('task/addmentor.html', {'form':form, 'errors':errors})
        
    else:
        return show_msg('You are not authorised to add mentors for this task', task_url, 'view the task')
    
def add_tasks(request, tid):
    """ first display tasks which can be subtasks for the task and do the rest.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = request.user
    task = Task.objects.get(id=tid)
    errors = []
    
    is_guest = True if not user.is_authenticated() else False
    
    if (not is_guest) and user in task.mentors.all():
        if task.status in ["OP", "LO"]:
            if request.method == "POST":
                ## first decide if adding subs and deps can be in same page
                ## only exclude tasks with status deleted
                pass
            else:
                ## write a form just like add mentor and get the form here
                pass
        else:
            errors = ["The task cannot be added subtasks or dependencies in this state"]
#            return render_to_response('task/add.html', {'form':form, 'errors':errors})
            return show_msg('The task cannot be added subtasks or dependencies now', task_url, 'view the task')
    else:
        return show_msg('You are not authorised to add subtasks or dependencies for this task', task_url, 'view the task')
    
    
def claim_task(request, tid):
    """ display a list of claims for get and display submit only if claimable """

    ## create claims model and create a new database with required tables for it
    ## see if that "one to n" or "n to one" relationship has a special field
    
    task_url = "/task/view/tid=%s"%tid
    claim_url = "/task/claim/tid=%s"%tid
    
    errors = []
    
    user = request.user
    task = Task.objects.get(id=tid)
    claims = Claim.objects.filter(task=task)
    
    is_guest = True if not user.is_authenticated() else False
    if user in task.mentors.all():
        is_mentor = True 
    else:
         is_mentor = False

    task_claimable = True if task.status in ["OP", "RE", "CL"] else False
    user_can_claim = True if  task_claimable and not ( is_guest or is_mentor ) and ( user not in task.claimed_users.all() )  else False
    task_claimed = True if task.status == "CL" else False
    
    context = {'is_mentor':is_mentor,
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
        return show_msg('You are not logged in to view claims for this task', task_url, 'view the task')
    
    
def assign_task(request, tid):
    """ first get the status of the task and then assign it to one of claimed users
    generate list of claimed users by passing it as an argument to a function.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = request.user
    task = Task.objects.get(id=tid)
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False

    task_claimed = True if task.status == "CL" else False
    
    if (not is_guest) and is_mentor:
        if task_claimed:
            user_list = ((user.id,user.username) for user in task.claimed_users.all())
            form = AssignTaskForm(user_list)
    
            if request.method == "POST":
                uid = request.POST['user']
                assigned_user = User.objects.get(id=uid)
                assignTask(task, assigned_user)
                return redirect(task_url)
            else:
                return render_to_response('task/assign.html',{'form':form})
        elif task.status == "AS":
            return show_msg('The task is already assigned', task_url, 'view the task')
        elif task.status == "OP":
            return show_msg('No one has still claimed the task', task_url, 'view the task')
        else:
            return show_msg('The task status is %s. how can you assign it now'%task.status, task_url, 'view the task')
    else:
        return show_msg('You are not authorised to perform this action', task_url, 'view the task')
        
def edit_task(request, tid):
    """ see what are the attributes that can be edited depending on the current status
    and then give the user fields accordingly.
    """
    
    return None

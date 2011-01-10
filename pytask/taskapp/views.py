from datetime import datetime

from django.contrib.auth.models import User

from django.shortcuts import render_to_response, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from pytask.utils import make_key
from pytask.views import show_msg

from pytask.taskapp.models import Task, TaskComment, TaskClaim, TextBook
from pytask.taskapp.forms import CreateTaskForm, EditTaskForm, \
                                 TaskCommentForm, ClaimTaskForm, \
                                 ChoiceForm, EditTaskForm, CreateTextbookForm
from pytask.taskapp.utils import getTask, getTextBook
from pytask.profile.utils import get_notification


@login_required
def create_task(request):

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }

    context.update(csrf(request))

    can_create_task = False if profile.rights == "CT" else True
    if can_create_task:
        if request.method == "POST":
            form = CreateTaskForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data.copy()
                data.update({"created_by": user,
                             "creation_datetime": datetime.now(),
                             "uniq_key": make_key(Task),
                            })
                
                task = Task(**data)
                task.save()

                task_url = '/task/view/tid=%s'%task.uniq_key
                return redirect(task_url)
            else:
                context.update({'form':form})
                return render_to_response('task/create.html', context)
        else:
            form = CreateTaskForm()
            context.update({'form':form})
            return render_to_response('task/create.html', context)
    else:
        return show_msg(user, 'You are not authorised to create a task.')

def view_task(request, tid):
    """ get the task depending on its tid and display accordingly if it is a get.
    check for authentication and add a comment if it is a post request.
    """
    
    task_url = "/task/view/tid=%s"%tid
    task = getTask(tid)

    user = request.user

    if not user.is_authenticated():
        return render_to_response("/task/view.html", {"task": task})

    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    if task.status == "DL":
        return show_msg(user, 'This task no longer exists', '/task/browse/','browse the tasks')

    task_viewable = True if ( task.status != "UP" ) or profile.rights != "CT"\
                         else False
    if not task_viewable:
        return show_msg(user, "You are not authorised to view this task", "/task/browse/", "browse the tasks")

    reviewers = task.reviewers.all()
    is_reviewer = True if user in task.reviewers.all() else False
    comments = task.comments.filter(is_deleted=False).order_by('comment_datetime')

    context.update({'is_reviewer':is_reviewer,
                    'comments':comments,
                    'reviewers':reviewers,
                   })

    claimed_users = task.claimed_users.all()
    selected_users = task.selected_users.all()

    is_creator = True if user == task.created_by else False
    has_claimed = True if user in claimed_users else False

    context['selected_users'] = selected_users
    context['is_selected'] = True if user in selected_users else False
    context['can_approve'] = True if task.status == "UP" and\
                                     profile.rights in ["MG", "DC"]\
                                     else False
    context['can_edit'] = True if is_creator and task.status == "UP" else False
    context['can_close'] = True if task.status not in ["UP", "CD", "CM"] and is_reviewer else False
    context['can_delete'] = True if task.status == "UP" and is_creator else False

    context['can_assign_pynts'] = True if task.status in ["OP", "WR"] and is_reviewer else False
    context['task_claimable'] = True if task.status in ["OP", "WR"] else False

    context['can_comment'] = True if task.status != "UP" or\
                                     profile.rights!="CT" else False

#    if task.status == "CD":
#        context['closing_notification'] =  Notification.objects.filter(task=task,role="CD")[0]
#    elif task.status == "CM":
#        context['completed_notification'] =  Notifications.objects.filter(task=task,role="CM")[0]
#    elif task.status == "WR":
#        context['assigned_users'] = task.assigned_users.all()
   
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            new_comment = TaskComment(task=task, data=data,
                                      uniq_key=make_key(TaskComment),
                                      commented_by=user, comment_datetime=datetime.now())
            new_comment.save()
            return redirect(task_url)
        else:
            context['form'] = form
            return render_to_response('task/view.html', context)
    else:
        form = TaskCommentForm()
        context['form'] = form
        return render_to_response('task/view.html', context)

@login_required
def edit_task(request, tid):
    """ only creator gets to edit the task and that too only before it gets
    approved.
    """

    user = request.user
    profile = user.get_profile()

    task_url = "/task/view/tid=%s"%tid
    task = getTask(tid)

    is_creator = True if user == task.created_by else False
    can_edit = True if task.status == "UP" and is_creator else False
    if not can_edit:
        raise Http404

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    if request.method == "POST":
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(task_url)
        else:
            context.update({"form": form})
            return render_to_response("task/edit.html", context)
    else:
        form = EditTaskForm(instance=task)
        context.update({"form": form})
        return render_to_response("task/edit.html", context)

@login_required
def create_textbook(request):

    user = request.user
    profile = user.get_profile()

    can_create = True if profile.rights != "CT" else False
    if not can_create:
        raise Http404

    context = {"user": user,
               "profile": profile,
              }

    context.update(csrf(request))

    if request.method == "POST":
        form = CreateTextbookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data.update({"uniq_key": make_key(TextBook),
                         "created_by": user,
                         "creation_datetime": datetime.now()})
            del data['chapters']
            new_textbook = TextBook(**data)
            new_textbook.save()

            new_textbook.chapters = form.cleaned_data['chapters']

            textbook_url = "/task/textbook/view/tid=%s"%new_textbook.uniq_key
            return redirect(textbook_url)
        else:
            context.update({"form": form})
            return render_to_response("task/create_textbook.html", context)
    else:
        form = CreateTextbookForm()
        context.update({"form": form})
        return render_to_response("task/create_textbook.html", context)

def view_textbook(request, tid):

    textbook = getTextBook(tid)
    textbook_url = "/task/textbook/view/tid=%s"%textbook.uniq_key

    user = request.user
    if not user.is_authenticated():
        return render_to_response("task/view_textbook.html", {"user": user})

    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
               "textbook": textbook,
              }

    context.update(csrf(request))

    chapters = Task.objects.filter(status="UP")

    can_edit = True if user == textbook.created_by and textbook.status == "UP"\
                       else False

    can_approve = True if profile.rights in ["MG", "DC"] and \
                          textbook.status == "UP" else False

    context.update({"chapters": chapters,
                    "can_edit": can_edit,
                    "can_approve": can_approve})
    return render_to_response("task/view_textbook.html", context)

def browse_textbooks(request):

    user = request.user

    open_textbooks = TextBook.objects.filter(status="OP").\
                                      order_by("creation_datetime")
    comp_textbooks = TextBook.objects.filter(status="CM").\
                                      order_by("creation_datetime")
    context = {"user": user,
               "open_textbooks": open_textbooks,
               "comp_textbooks": comp_textbooks,
              }

    if user.is_authenticated() and user.get_profile().rights != "CT":
        unpub_textbooks = TextBook.objects.filter(status="UP")

        context.update({"unpub_textbooks": unpub_textbooks})

    return render_to_response("task/browse_textbooks.html", context)

@login_required
def claim_task(request, tid):

    task_url = "/task/view/tid=%s"%tid
    claim_url = "/task/claim/tid=%s"%tid
    task = getTask(tid)

    if task.status == "UP":
        raise Http404

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    reviewers = task.reviewers.all()
    claimed_users = task.claimed_users.all()
    selected_users = task.selected_users.all()

    is_creator = True if user == task.created_by else False
    is_reviewer = True if user in reviewers else False
    has_claimed = True if user in claimed_users else False

    task_claimable = True if task.status in ["OP", "WR"] else False
    can_claim = True if task_claimable and ( not has_claimed )\
                        and ( not is_reviewer ) and (not is_creator ) \
                        else False

    old_claims = task.claims.all()

    context.update({"is_creator": is_creator,
                    "task_claimable": task_claimable,
                    "can_claim": can_claim,
                    "old_claims": old_claims})

    if request.method == "POST" and can_claim:
        form = ClaimTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data.update({"uniq_key": make_key(TaskClaim),
                         "task": task,
                         "claim_datetime": datetime.now(),
                         "claimed_by": user,})
            new_claim = TaskClaim(**data)
            new_claim.save()

            task.claimed_users.add(user)
            task.save()

            return redirect(claim_url)

        else:
            context.update({"form": form})
            return render_to_response("task/claim.html", context)
    else:
        form = ClaimTaskForm()
        context.update({"form": form})
        return render_to_response("task/claim.html", context)

@login_required
def select_user(request, tid):
    """ first get the status of the task and then select one of claimed users
    generate list of claimed users by passing it as an argument to a function.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = request.user
    profile = user.get_profile()
    task = getTask(tid)
    
    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    claimed_users = task.claimed_users.all()
    selected_users = task.selected_users.all()
    task_claimed = True if claimed_users else False
    
    is_creator = True if user == task.created_by else False

    if ( is_creator or profile.rights in ["CR", "DC"] ) and \
       task.status in ["OP", "WR"]:

        if task_claimed:

            user_list = ((user.id,user.username) for user in claimed_users)

            if request.method == "POST":
                form = ChoiceForm(user_list, request.POST)
                if form.is_valid():
                    uid = form.cleaned_data['choice']
                    selected_user = User.objects.get(id=uid)

                    task.selected_users.add(selected_user)
                    task.claimed_users.remove(selected_user)
                    task.status = "WR"
                    task.save()

                    return redirect(task_url)
                else:
                    context.update({"form": form})
                    return render_to_response('task/select_user.html', context)
            else:
                form = ChoiceForm(user_list)
                context.update({"form": form})
                return render_to_response('task/select_user.html', context)
        else:
            return show_msg(user, 'There are no pending claims for this task',
                            task_url, 'view the task')
    else:
        raise Http404


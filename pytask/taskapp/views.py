from datetime import datetime

from django import shortcuts
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from pytask.views import show_msg

from pytask.taskapp import forms as taskapp_forms
from pytask.taskapp import models as taskapp_models


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
            form = taskapp_forms.CreateTaskForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data.copy()
                data.update({"created_by": user,
                             "creation_datetime": datetime.now(),
                            })

                task = taskapp_models.Task(**data)
                task.save()

                task_url = reverse('view_task', kwargs={'task_id': task.id})
                return shortcuts.redirect(task_url)
            else:
                context.update({'form':form})
                return shortcuts.render_to_response(
                  'task/create.html', context)
        else:
            form = taskapp_forms.CreateTaskForm()
            context.update({'form': form})
            return shortcuts.render_to_response('task/create.html', context)
    else:
        return show_msg(user, 'You are not authorised to create a task.')

def browse_tasks(request):

    open_tasks = taskapp_models.Task.objects.filter(status="OP")
    working_tasks = taskapp_models.Task.objects.filter(status="WR")
    comp_tasks = taskapp_models.Task.objects.filter(status="CM")

    context = {"open_tasks": open_tasks,
               "working_tasks": working_tasks,
               "comp_tasks": comp_tasks,
              }

    user = request.user
    if not user.is_authenticated():
        return shortcuts.render_to_response("task/browse.html")

    profile = user.get_profile()

    can_approve = True if profile.rights in ["MG", "DC"] else False
    unpub_tasks = taskapp_models.Task.objects.filter(status="UP").exclude(status="DL")
    if can_approve:
        context.update({"unpub_tasks": unpub_tasks})

    context.update({"user": user,
                    "profile": profile,
                   })

    return shortcuts.render_to_response("task/browse.html", context)


def view_task(request, task_id):
    """ get the task depending on its task_id and display accordingly if it is a get.
    check for authentication and add a comment if it is a post request.
    """

    task_url = reverse('view_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    user = request.user

    if not user.is_authenticated():
        return shortcuts.render_to_response("task/view.html", {"task": task})

    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    if task.status == "DL":
        return show_msg(user, 'This task no longer exists',
                        reverse('browse_tasks'), 'browse the tasks')

    task_viewable = True if ( task.status != "UP" ) or profile.rights != "CT"\
                         else False
    if not task_viewable:
        return show_msg(user, "You are not authorised to view this task",
                        reverse('browse_tasks'), "browse the tasks")

    reviewers = task.reviewers.all()
    is_reviewer = True if user in task.reviewers.all() else False
    comments = task.comments.filter(
      is_deleted=False).order_by('comment_datetime')

    context.update({'is_reviewer':is_reviewer,
                    'comments':comments,
                    'reviewers':reviewers,
                   })

    selected_users = task.selected_users.all()

    is_creator = True if user == task.created_by else False

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

    context['can_mod_reviewers'] = True if profile.rights in ["MG", "DC"] else\
                                   False

    if request.method == 'POST':
        form = taskapp_forms.TaskCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            new_comment = taskapp_forms.TaskComment(
              task=task, data=data, commented_by=user,
              comment_datetime=datetime.now())
            new_comment.save()
            return shortcuts.redirect(task_url)
        else:
            context['form'] = form
            return shortcuts.render_to_response('task/view.html', context)
    else:
        form = taskapp_forms.TaskCommentForm()
        context['form'] = form
        return shortcuts.render_to_response('task/view.html', context)

@login_required
def edit_task(request, task_id):
    """ only creator gets to edit the task and that too only before it gets
    approved.
    """

    user = request.user
    profile = user.get_profile()

    task_url = reverse('view_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    is_creator = True if user == task.created_by else False
    can_edit = True if task.status == "UP" and is_creator else False
    if not can_edit:
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    if request.method == "POST":
        form = taskapp_forms.EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return shortcuts.redirect(task_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response("task/edit.html", context)
    else:
        form = taskapp_forms.EditTaskForm(instance=task)
        context.update({"form": form})
        return shortcuts.render_to_response("task/edit.html", context)

@login_required
def approve_task(request, task_id):

    user = request.user
    profile = user.get_profile()

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if profile.rights not in ["MG", "DC"] or task.status != "UP":
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    return shortcuts.render_to_response("task/confirm_approval.html", context)

@login_required
def approved_task(request, task_id):

    user = request.user
    profile = user.get_profile()

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if profile.rights not in ["MG", "DC"] or task.status != "UP":
        raise http.Http404

    task.approved_by = user
    task.approval_datetime = datetime.now()
    task.status = "OP"
    task.save()

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    return shortcuts.render_to_response("task/approved_task.html", context)

@login_required
def addreviewer(request, task_id):

    user = request.user
    profile = user.get_profile()

    task_url = reverse('view_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    can_mod_reviewers = True if profile.rights in ["MG", "DC"] else False
    if not can_mod_reviewers:
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))


    # This part has to be made better
    reviewer_choices = User.objects.filter(is_active=True).\
                                           exclude(reviewing_tasks__id=task_id).\
                                           exclude(claimed_tasks__id=task_id).\
                                           exclude(selected_tasks__id=task_id).\
                                           exclude(created_tasks__id=task_id)

    choices = ((a_user.id,a_user.username) for a_user in reviewer_choices)
    label = "Reviewer"

    if request.method == "POST":
        form = taskapp_forms.ChoiceForm(choices, data=request.POST, label=label)
        if form.is_valid():
            data = form.cleaned_data.copy()
            uid = data['choice']
            reviewer = User.objects.get(id=uid)

            task.reviewers.add(reviewer)
            return shortcuts.redirect(task_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response("task/addreviewer.html", context)
    else:
        form = taskapp_forms.ChoiceForm(choices, label=label)
        context.update({"form": form})
        return shortcuts.render_to_response("task/addreviewer.html", context)

def view_work(request, task_id):

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    user = request.user
    old_reports = task.reports.all()

    context = {"task": task,
               "old_reports": old_reports,
              }

    if not user.is_authenticated():
        return shortcuts.render_to_response("task/view_work.html", context)

    profile = user.get_profile()

    context.update({"user": user,
                    "profile": profile,
                   })

    context.update(csrf(request))

    working_users = task.selected_users.all()
    is_working = True if user in working_users else False

    context.update({"is_working": is_working})

    return shortcuts.render_to_response("task/view_work.html", context)

@login_required
def view_report(request, report_id):

    report = shortcuts.get_object_or_404(taskapp_models.WorkReport,
                                         pk=report_id)

    user = request.user
    context = {"report": report,
               "user": user,
              }

    if not user.is_authenticated():
        return shortcuts.render_to_response("task/view_report.html", context)

    profile = user.get_profile()

    context.update({"profile": profile})
    return shortcuts.render_to_response("task/view_report.html", context)

@login_required
def submit_report(request, task_id):
    """ Check if the work is in WR state and the user is in assigned_users.
    """
    task_url = reverse('view_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    user = request.user
    old_reports = task.reports.all()

    if not task.status == "WR":
        raise http.Http404

    can_upload = True if user in task.selected_users.all() else False

    context = {
        'user': user,
        'task': task,
        'can_upload': can_upload,
    }

    context.update(csrf(request))

    if request.method == "POST":
        if not can_upload:
            return show_msg(user, "You are not authorised to upload data to this task", task_url, "view the task")

        form = taskapp_forms.WorkReportForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data.copy()
            data.update({"task":task,
                         "revision": old_reports.count(),
                         "submitted_by": user,
                         "submitted_at": datetime.now(),
                        })
            r = taskapp_models.WorkReport(**data)
            r.save()

            report_url = reverse('view_report', kwargs={'report_id': r.id})
            return shortcuts.redirect(report_url)

        else:
            context.update({"form":form})
            return shortcuts.render_to_response('task/submit_report.html', context)

    else:
        form = taskapp_forms.WorkReportForm()
        context.update({"form":form})
        return shortcuts.render_to_response('task/submit_report.html', context)

@login_required
def create_textbook(request):

    user = request.user
    profile = user.get_profile()

    can_create = True if profile.rights != "CT" else False
    if not can_create:
        raise http.Http404

    context = {"user": user,
               "profile": profile,
              }

    context.update(csrf(request))

    if request.method == "POST":
        form = taskapp_forms.CreateTextbookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data.update({"created_by": user,
                         "creation_datetime": datetime.now()})
            del data['chapters']
            new_textbook = taskapp_models.TextBook(**data)
            new_textbook.save()

            new_textbook.chapters = form.cleaned_data['chapters']

            textbook_url = reverse(
              'view_textbook', kwargs={'task_id': new_textbook.id})
            return shortcuts.redirect(textbook_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response("task/create_textbook.html", context)
    else:
        form = taskapp_forms.CreateTextbookForm()
        context.update({"form": form})
        return shortcuts.render_to_response("task/create_textbook.html", context)

def view_textbook(request, task_id):

    textbook = shortcuts.get_object_or_404(taskapp_models.TextBook, pk=task_id)
    chapters = textbook.chapters.all()

    user = request.user

    context = {"user": user,
               "textbook": textbook,
               "chapters": chapters,
              }

    if not user.is_authenticated():
        return shortcuts.render_to_response("task/view_textbook.html", context)

    profile = user.get_profile()

    context.update({"profile": profile,
                    "textbook": textbook,
                   })

    context.update(csrf(request))

    can_edit = True if user == textbook.created_by and textbook.status == "UP"\
                       else False

    can_approve = True if profile.rights in ["MG", "DC"] and \
                          textbook.status == "UP" else False

    context.update({"can_edit": can_edit,
                    "can_approve": can_approve})
    return shortcuts.render_to_response("task/view_textbook.html", context)

def browse_textbooks(request):

    user = request.user

    open_textbooks = taskapp_models.TextBook.objects.filter(status="OP").\
                                      order_by("creation_datetime")
    comp_textbooks = taskapp_models.TextBook.objects.filter(status="CM").\
                                      order_by("creation_datetime")
    context = {"user": user,
               "open_textbooks": open_textbooks,
               "comp_textbooks": comp_textbooks,
              }

    if user.is_authenticated() and user.get_profile().rights in ["DC", "MG"]:
        unpub_textbooks = taskapp_models.TextBook.objects.filter(status="UP")

        context.update({"unpub_textbooks": unpub_textbooks})

    return shortcuts.render_to_response("task/browse_textbooks.html", context)

@login_required
def edit_textbook(request, task_id):

    user = request.user
    profile = user.get_profile()

    textbook = shortcuts.get_object_or_404(taskapp_models.TextBook, pk=task_id)
    textbook_url = reverse(
      'view_textbook', kwargs={'task_id': textbook.id})

    can_edit = True if user == textbook.created_by and textbook.status == "UP"\
                       else False

    if not can_edit:
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "textbook": textbook,
              }

    context.update(csrf(request))

    if request.method == "POST":
        form = taskapp_forms.EditTextbookForm(request.POST, instance=textbook)
        if form.is_valid():
            form.save()
            return shortcuts.redirect(textbook_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response("task/edit_textbook.html", context)
    else:
        form = taskapp_forms.EditTextbookForm(instance=textbook)
        context.update({"form": form})
        return shortcuts.render_to_response("task/edit_textbook.html", context)

@login_required
def claim_task(request, task_id):

    claim_url = "/task/claim/task_id=%s"%task_id
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if task.status == "UP":
        raise http.Http404

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    reviewers = task.reviewers.all()
    claimed_users = task.claimed_users.all()

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
        form = taskapp_forms.ClaimTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data.update({"task": task,
                         "claim_datetime": datetime.now(),
                         "claimed_by": user,})
            new_claim = taskapp_models.TaskClaim(**data)
            new_claim.save()

            task.claimed_users.add(user)
            task.save()

            return shortcuts.redirect(claim_url)

        else:
            context.update({"form": form})
            return shortcuts.render_to_response("task/claim.html", context)
    else:
        form = taskapp_forms.ClaimTaskForm()
        context.update({"form": form})
        return shortcuts.render_to_response("task/claim.html", context)

@login_required
def select_user(request, task_id):
    """ first get the status of the task and then select one of claimed users
    generate list of claimed users by passing it as an argument to a function.
    """

    task_url = reverse('view_task', kwargs={'task_id': task_id})

    user = request.user
    profile = user.get_profile()
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    context.update(csrf(request))

    claimed_users = task.claimed_users.all()
    task_claimed = True if claimed_users else False
    
    is_creator = True if user == task.created_by else False

    if ( is_creator or profile.rights in ["CR", "DC"] ) and \
       task.status in ["OP", "WR"]:

        if task_claimed:

            user_list = ((user.id,user.username) for user in claimed_users)

            if request.method == "POST":
                form = taskapp_forms.ChoiceForm(user_list, request.POST)
                if form.is_valid():
                    uid = form.cleaned_data['choice']
                    selected_user = User.objects.get(id=uid)

                    task.selected_users.add(selected_user)
                    task.claimed_users.remove(selected_user)
                    task.status = "WR"
                    task.save()

                    return shortcuts.redirect(task_url)
                else:
                    context.update({"form": form})
                    return shortcuts.render_to_response('task/select_user.html', context)
            else:
                form = taskapp_forms.ChoiceForm(user_list)
                context.update({"form": form})
                return shortcuts.render_to_response('task/select_user.html', context)
        else:
            return show_msg(user, 'There are no pending claims for this task',
                            task_url, 'view the task')
    else:
        raise http.Http404

@login_required
def approve_textbook(request, task_id):

    user = request.user
    profile = user.get_profile()

    textbook = shortcuts.get_object_or_404(taskapp_models.TextBook, pk=task_id)

    if profile.rights not in ["MG", "DC"] or textbook.status != "UP":
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "textbook": textbook,
              }

    return shortcuts.render_to_response("task/confirm_textbook_approval.html", context)

@login_required
def approved_textbook(request, task_id):

    user = request.user
    profile = user.get_profile()

    textbook = shortcuts.get_object_or_404(taskapp_models.TextBook, pk=task_id)

    if profile.rights not in ["MG", "DC"] or textbook.status != "UP":
        raise http.Http404

    textbook.approved_by = user
    textbook.approval_datetime = datetime.now()
    textbook.status = "OP"
    textbook.save()

    context = {"user": user,
               "profile": profile,
               "textbook": textbook,
              }

    return shortcuts.render_to_response("task/approved_textbook.html", context)

def suggest_task_tags(request):
    """Returns the tags matching the query for the AJAXy autocomplete
    to get tags related to tasks.
    """

    taskapp_models.Task.objects.filter(tags)
    json_response = json.dumps(['abc', 'bca', 'bowbow'])
    return http.HttpResponse(json_response)

#!/usr/bin/env python
#
# Copyright 2011 Authors of PyTask.
#
# This file is part of PyTask.
#
# PyTask is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyTask is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTask.  If not, see <http://www.gnu.org/licenses/>.


"""Module containing the views for all the task related activities.

If there is something common to all other views. They sit here, here
even if there nothing relevant to tasks alone since task is the basis
for everything else.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    ]


from datetime import datetime

from django import shortcuts
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson as json
from django.utils.translation import ugettext

from tagging.models import Tag
from tagging.models import TaggedItem

from pytask.helpers import exceptions
from pytask.views import show_msg

from pytask.profile import models as profile_models

from pytask.taskapp import forms as taskapp_forms
from pytask.taskapp import models as taskapp_models


DONT_CLAIM_TASK_MSG = ugettext(
  "Please don't submit any claims for the tasks until you get an email "
  "to start claiming tasks. Please be warned that the task claim work-"
  "flow may change. So all the claims submitted before the workshop may "
  "not be valid.")

NO_EDIT_RIGHT = ugettext(
  "You are not authorized to edit this page.")

NO_MOD_REVIEWERS_RIGHT = ugettext(
  "You are not authorized to moderate reviewers.")

NO_SELECT_USER = ugettext(
  "You are not authorized to approve task claims.")


@login_required
def create_task(request):

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }

    context.update(csrf(request))

    can_create_task = False if (
      profile.role == profile_models.ROLES_CHOICES[3][0]) else True
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
                  'task/edit.html', RequestContext(request, context))
        else:
            form = taskapp_forms.CreateTaskForm()
            context.update({'form': form})
            return shortcuts.render_to_response(
              'task/edit.html', RequestContext(request, context))
    else:
        return show_msg(user, 'You are not authorised to create a task.')

def browse_tasks(request):

    context = {}

    open_tasks = taskapp_models.Task.objects.filter(
      status=taskapp_models.TASK_STATUS_CHOICES[1][0])
    working_tasks = taskapp_models.Task.objects.filter(
      status=taskapp_models.TASK_STATUS_CHOICES[3][0])
    comp_tasks = taskapp_models.Task.objects.filter(
      status=taskapp_models.TASK_STATUS_CHOICES[6][0])

    context.update({
      'open_tasks': open_tasks,
      'working_tasks': working_tasks,
      'comp_tasks': comp_tasks,
      })

    user = request.user
    if not user.is_authenticated():
        return shortcuts.render_to_response('task/browse.html',
                                            RequestContext(request, context))

    profile = user.get_profile()


    if profile.role in [profile_models.ROLES_CHOICES[0][0],
                        profile_models.ROLES_CHOICES[1][0]]:
        can_approve = True
    else:
        can_approve = False

    unpub_tasks = taskapp_models.Task.objects.filter(
      status=taskapp_models.TASK_STATUS_CHOICES[0][0]).exclude(
        status=taskapp_models.TASK_STATUS_CHOICES[5][0])

    if can_approve:
        context.update({'unpub_tasks': unpub_tasks})

    context.update({'user': user,
                    'profile': profile,
                   })

    return shortcuts.render_to_response('task/browse.html',
                                        RequestContext(request, context))


def view_task(request, task_id, **kwargs):
    """View to get the requested.

    Checks for authentication and add a comment if it is a post request.
    """

    context = {}

    if 'context' in kwargs:
        context.update(kwargs['context'])

    task_url = kwargs.get(
      'task_url', reverse('view_task', kwargs={'task_id': task_id}))

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    user = request.user

    if not user.is_authenticated():
        return shortcuts.render_to_response('task/view.html', {'task': task})

    profile = user.get_profile()

    context.update({
      'user': user,
      'profile': profile,
      'task': task,
      })

    context.update(csrf(request))

    if task.status == taskapp_models.TASK_STATUS_CHOICES[5][0]:
        return show_msg(user, 'This task no longer exists',
                        reverse('browse_tasks'), 'browse the tasks')

    if ((task.status != taskapp_models.TASK_STATUS_CHOICES[0][0] )
      or profile.role != profile_models.ROLES_CHOICES[3][0]):
        task_viewable = True
    else:
        task_viewable = False

    if not task_viewable:
        return show_msg(user, 'You are not authorised to view this task',
                        reverse('browse_tasks'), 'browse the tasks')

    reviewers = task.reviewers.all()
    is_reviewer = True if user in task.reviewers.all() else False
    comments = task.comments.filter(
      is_deleted=False).order_by('comment_datetime')

    context.update({'is_reviewer':is_reviewer,
                    'comments':comments,
                    'reviewers':reviewers,
                   })

    selected_users = task.selected_users.all()

    user_role = user.get_profile().role
    is_creator = True if user == task.created_by else False

    context['selected_users'] = selected_users

    context['is_selected'] = True if user in selected_users else False

    if (task.status == taskapp_models.TASK_STATUS_CHOICES[0][0] and
      profile.role in [profile_models.ROLES_CHOICES[0][0],
      profile_models.ROLES_CHOICES[1][0]]):
        context['can_approve'] = True
    else:
        context['can_approve'] = False

    if ((is_creator or user_role != profile_models.ROLES_CHOICES[3][0])
      and task.status in [taskapp_models.TASK_STATUS_CHOICES[0][0],
      taskapp_models.TASK_STATUS_CHOICES[1][0]]):
        context['can_edit'] = True
    else:
        context['can_edit'] = False

    if (task.status not in [taskapp_models.TASK_STATUS_CHOICES[0][0],
      taskapp_models.TASK_STATUS_CHOICES[4][0],
      taskapp_models.TASK_STATUS_CHOICES[6][0]] and is_reviewer):
        context['can_close'] = True
    else:
        context['can_close'] = False

    if task.status == taskapp_models.TASK_STATUS_CHOICES[0][0] and is_creator:
        context['can_delete'] = True
    else:
        context['can_delete'] = False

    if (task.status in [taskapp_models.TASK_STATUS_CHOICES[1][0],
      taskapp_models.TASK_STATUS_CHOICES[3][0]] and is_reviewer):
        context['can_assign_pynts'] = True
    else:
        context['can_assign_pynts'] = False

    if (task.status in [taskapp_models.TASK_STATUS_CHOICES[1][0],
      taskapp_models.TASK_STATUS_CHOICES[3][0]]):
        context['task_claimable'] = True
    else:
        context['task_claimable'] = False

    if (task.status != taskapp_models.TASK_STATUS_CHOICES[0][0] or\
      profile.role != profile_models.ROLES_CHOICES[3][0]):
        context['can_comment'] = True
    else:
        context['can_comment'] = False

    if (profile.role in [profile_models.ROLES_CHOICES[0][0],
      profile_models.ROLES_CHOICES[1][0]]):
        context['can_mod_reviewers'] = True
    else:
        context['can_mod_reviewers'] = False

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
            return shortcuts.render_to_response(
              'task/view.html', RequestContext(request, context))
    else:
        form = taskapp_forms.TaskCommentForm()
        context['form'] = form
        return shortcuts.render_to_response(
          'task/view.html', RequestContext(request, context))

@login_required
def edit_task(request, task_id, **kwargs):
    """ only creator gets to edit the task and that too only before it gets
    approved.
    """

    user = request.user
    profile = user.get_profile()

    task_url = kwargs.get(
      'task_url', reverse('view_task', kwargs={'task_id': task_id}))
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    is_creator = True if user == task.created_by else False

    if ((is_creator or profile.role != profile_models.ROLES_CHOICES[3][0])
      and task.status in [taskapp_models.TASK_STATUS_CHOICES[0][0],
      taskapp_models.TASK_STATUS_CHOICES[1][0]]):
        can_edit = True 
    else:
        can_edit = False

    if not can_edit:
        raise exceptions.UnauthorizedAccess(NO_EDIT_RIGHT)

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
            return shortcuts.render_to_response(
              "task/edit.html", RequestContext(request, context))
    else:
        form = taskapp_forms.EditTaskForm(instance=task)
        context.update({"form": form})
        return shortcuts.render_to_response("task/edit.html",
                                            RequestContext(request, context))

@login_required
def approve_task(request, task_id):

    user = request.user
    profile = user.get_profile()

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if (profile.role not in [profile_models.ROLES_CHOICES[0][0],
      profile_models.ROLES_CHOICES[1][0]] or
      task.status != taskapp_models.TASK_STATUS_CHOICES[0][0]):
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    return shortcuts.render_to_response(
      "task/confirm_approval.html", RequestContext(request, context))

@login_required
def approved_task(request, task_id):

    user = request.user
    profile = user.get_profile()

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if profile.role not in [profile_models.ROLES_CHOICES[0][0], profile_models.ROLES_CHOICES[1][0]] or task.status != taskapp_models.TASK_STATUS_CHOICES[0][0]:
        raise http.Http404

    task.approved_by = user
    task.approval_datetime = datetime.now()
    task.status = taskapp_models.TASK_STATUS_CHOICES[1][0]
    task.save()

    context = {"user": user,
               "profile": profile,
               "task": task,
              }

    return shortcuts.render_to_response(
      "task/approved_task.html", RequestContext(request, context))

@login_required
def addreviewer(request, task_id, template_name='task/addreviewer.html'):

    user = request.user
    profile = user.get_profile()

    task_url = reverse('view_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if profile.role in [profile_models.ROLES_CHOICES[0][0],
      profile_models.ROLES_CHOICES[1][0]]:
        can_mod_reviewers = True
    else:
        can_mod_reviewers = False

    if not can_mod_reviewers:
        raise exceptions.UnauthorizedAccess(NO_MOD_REVIEWERS_RIGHT)

    context = {
      'user': user,
      'profile': profile,
      'task': task,
      }

    context.update(csrf(request))


    # TODO(Madhu): This part has to be made better
    reviewer_choices = User.objects.filter(
      is_active=True).exclude(reviewing_tasks__id=task_id).exclude(
      claimed_tasks__id=task_id).exclude(
      selected_tasks__id=task_id).exclude(created_tasks__id=task_id)

    choices = ((a_user.id, a_user.username) for a_user in reviewer_choices)
    label = "Reviewer"

    if request.method == "POST":
        form = taskapp_forms.ChoiceForm(
          choices, data=request.POST, label=label)
        if form.is_valid():
            data = form.cleaned_data.copy()
            uid = data['choice']
            reviewer = User.objects.get(id=uid)

            task.reviewers.add(reviewer)
            return shortcuts.redirect(task_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response(
              template_name, RequestContext(request, context))
    else:
        form = taskapp_forms.ChoiceForm(choices, label=label)
        context.update({"form": form})
        return shortcuts.render_to_response(
          template_name, RequestContext(request, context))

def view_work(request, task_id):

    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    user = request.user
    old_reports = task.reports.all()

    context = {
      'task': task,
      'old_reports': old_reports,
      }

    if not user.is_authenticated():
        return shortcuts.render_to_response(
          "task/view_work.html", RequestContext(request, context))

    profile = user.get_profile()

    context.update({"user": user,
                    "profile": profile,
                   })

    context.update(csrf(request))

    working_users = task.selected_users.all()
    is_working = True if user in working_users else False

    context.update({"is_working": is_working})

    return shortcuts.render_to_response("task/view_work.html",
                                        RequestContext(request, context))

@login_required
def view_report(request, report_id):

    report = shortcuts.get_object_or_404(taskapp_models.WorkReport,
                                         pk=report_id)

    user = request.user
    context = {"report": report,
               "user": user,
              }

    if not user.is_authenticated():
        return shortcuts.render_to_response(
          "task/view_report.html", RequestContext(request, context))

    profile = user.get_profile()

    context.update({"profile": profile})
    return shortcuts.render_to_response("task/view_report.html",
                                        RequestContext(request, context))

@login_required
def submit_report(request, task_id):
    """ Check if the work is in WR state and the user is in assigned_users.
    """
    task_url = reverse('view_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    user = request.user
    old_reports = task.reports.all()

    if not task.status == taskapp_models.TASK_STATUS_CHOICES[3][0]:
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
            return shortcuts.render_to_response(
              'task/submit_report.html', RequestContext(request, context))

    else:
        form = taskapp_forms.WorkReportForm()
        context.update({"form":form})
        return shortcuts.render_to_response(
          'task/submit_report.html', RequestContext(request, context))

@login_required
def claim_task(request, task_id, template_name='task/claim.html'):

    context = {}

    claim_url = reverse('claim_task', kwargs={'task_id': task_id})
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    if task.status == taskapp_models.TASK_STATUS_CHOICES[0][0]:
        raise http.Http404

    user = request.user
    profile = user.get_profile()

    context.update({
      'user': user,
      'profile': profile,
      'task': task,
      })

    context.update(csrf(request))

    reviewers = task.reviewers.all()
    claimed_users = task.claimed_users.all()

    is_creator = True if user == task.created_by else False
    is_reviewer = True if user in reviewers else False
    has_claimed = True if user in claimed_users else False

    if task.status in [taskapp_models.TASK_STATUS_CHOICES[1][0],
      taskapp_models.TASK_STATUS_CHOICES[3][0]]:
        task_claimable = True
    else:
        task_claimable = False

    if (task_claimable and not has_claimed
      and not is_reviewer and not is_creator):
        can_claim = True
    else:
        can_claim =False

    if (is_creator or is_reviewer or profile.role in
      [profile_models.ROLES_CHOICES[0][0],
      profile_models.ROLES_CHOICES[1][0]]):
        can_approve = True
    else:
        can_approve = False

    old_claims = task.claims.all()

    context.update({
      'can_approve': can_approve,
      'task_claimable': task_claimable,
      'can_claim': can_claim,
      'old_claims': old_claims
      })

    if request.method == 'POST' and can_claim:
        form = taskapp_forms.ClaimTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data.update({
              'task': task,
              'claim_datetime': datetime.now(),
              'claimed_by': user,})
            new_claim = taskapp_models.TaskClaim(**data)
            new_claim.save()

            task.claimed_users.add(user)
            task.save()

            return shortcuts.redirect(claim_url)

        else:
            context.update({'form': form})
            return shortcuts.render_to_response(
              template_name, RequestContext(request, context))
    else:
        form = taskapp_forms.ClaimTaskForm()
        context.update({'form': form})
        return shortcuts.render_to_response(
          template_name, RequestContext(request, context))

@login_required
def select_user(request, task_id):
    """ first get the status of the task and then select one of claimed users
    generate list of claimed users by passing it as an argument to a function.
    """

    task_url = reverse('view_task', kwargs={'task_id': task_id})

    user = request.user
    profile = user.get_profile()
    task = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)

    context = {
      'user': user,
      'profile': profile,
      'task': task,
      }

    context.update(csrf(request))

    reviewers = task.reviewers.all()
    claimed_users = task.claimed_users.all()

    is_reviewer = True if user in reviewers else False
    task_claimed = True if claimed_users else False

    is_creator = True if user == task.created_by else False

    if (is_creator or is_reviewer  or profile.role in
      [profile_models.ROLES_CHOICES[0][0], profile_models.ROLES_CHOICES[1][0]]
      and task.status in [taskapp_models.TASK_STATUS_CHOICES[1][0],
      taskapp_models.TASK_STATUS_CHOICES[3][0]]):

        if task_claimed:

            user_list = ((user.id,user.username) for user in claimed_users)

            if request.method == "POST":
                form = taskapp_forms.ChoiceForm(user_list, request.POST)
                if form.is_valid():
                    uid = form.cleaned_data['choice']
                    selected_user = User.objects.get(id=uid)

                    task.selected_users.add(selected_user)
                    task.claimed_users.remove(selected_user)
                    task.status = taskapp_models.TASK_STATUS_CHOICES[3][0]
                    task.save()

                    return shortcuts.redirect(task_url)
                else:
                    context.update({"form": form})
                    return shortcuts.render_to_response(
                      'task/select_user.html',
                      RequestContext(request, context))
            else:
                form = taskapp_forms.ChoiceForm(user_list)
                context.update({"form": form})
                return shortcuts.render_to_response(
                  'task/select_user.html',
                  RequestContext(request, context))
        else:
            return show_msg(user, 'There are no pending claims for this task',
                            task_url, 'view the task')
    else:
        raise exceptions.UnauthorizedAccess(NO_SELECT_USER)

def suggest_task_tags(request):
    """Returns the tags matching the query for the AJAXy autocomplete
    to get tags related to tasks.
    """

    term = request.GET.get('term', None)
    response = []

    if term:
      tag_entities = Tag.objects.filter(name__icontains=term)
      response = [tag.name for tag in tag_entities]

    json_response = json.dumps(response)
    return http.HttpResponse(json_response)

def view_tag(request, tag_name, template='task/view_tag.html'):
    """View that displays all the tasks tagged with the given name
    """

    tag = Tag.objects.filter(name=tag_name)
    tasks = TaggedItem.objects.get_by_model(taskapp_models.Task, tag)

    context = {
      'tag_name': tag_name,
      'tasks': tasks,
      }

    return shortcuts.render_to_response(
      template, RequestContext(request, context))

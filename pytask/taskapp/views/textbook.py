"""Module containing the views for all the textbook project related activities.

"""

__authors__ = [
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from datetime import datetime

from django import shortcuts
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.translation import ugettext

from tagging.managers import TaggedItem

from pytask.helpers import exceptions

from pytask.profile import models as profile_models

from pytask.taskapp import forms as taskapp_forms
from pytask.taskapp import models as taskapp_models
from pytask.taskapp.views import task as task_view
from pytask.taskapp.views.utils import get_intial_tags_for_chapter


DONT_CLAIM_TASK_MSG = ugettext(
  "Please don't submit any claims for the tasks until you get an email "
  "to start claiming tasks. Please be warned that the task claim work-"
  "flow may change. So all the claims submitted before the workshop may "
  "not be valid.")

NO_EDIT_RIGHT = ugettext(
  "You are not authorized to edit this page.")

NOT_A_PARENT_FOR_CHAPTER = ugettext(
  "There is an error in your request. The chapter you are requesting is "
  "does not belong to the textbook you have requested.")


@login_required
def create_textbook(request):

    user = request.user
    profile = user.get_profile()

    if profile.role != profile_models.ROLES_CHOICES[3][0]:
        can_create = True
    else:
        can_create= False

    if not can_create:
        raise http.HttpResponseForbidden

    context = {
      'user': user,
      'profile': profile,
      }

    context.update(csrf(request))

    if request.method == 'POST':
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
            return shortcuts.render_to_response(
              "task/edit.html", RequestContext(request, context))
    else:
        form = taskapp_forms.CreateTextbookForm()
        context.update({"form": form})
        return shortcuts.render_to_response(
          "task/edit.html", RequestContext(request, context))

def view_textbook(request, task_id, template='task/view_textbook.html'):

    # Shortcut to get_object_or_404 is not used since django-tagging
    # api expects a queryset object for tag filtering.
    task = taskapp_models.Task.objects.filter(pk=task_id)

    textbooks = TaggedItem.objects.get_by_model(task, ['Textbook'])

    if textbooks:
        textbook = textbooks[0]
    else:
        raise http.Http404

    chapters = textbook.children_tasks.all()

    user = request.user

    context = {
      'user': user,
      'textbook': textbook,
      'chapters': chapters,
      }

    if not user.is_authenticated():
        return shortcuts.render_to_response(template,
                                            RequestContext(request, context))

    profile = user.get_profile()

    context.update({
      'profile': profile,
      'textbook': textbook,
      })

    context.update(csrf(request))

    user_role = user.get_profile().role
    if ((user == textbook.created_by or
      user_role != profile_models.ROLES_CHOICES[3][0]) and
      textbook.status in [taskapp_models.TB_STATUS_CHOICES[0][0],
      taskapp_models.TB_STATUS_CHOICES[1][0]]):
        can_edit = True
        can_create_chapters = True
    else:
        can_edit = False
        can_create_chapters = False

    if (profile.role in [profile_models.ROLES_CHOICES[0][0],
      profile_models.ROLES_CHOICES[1][0]] and
      textbook.status == taskapp_models.TB_STATUS_CHOICES[0][0]):
        can_approve = True
    else:
        can_approve = False

    context.update({
      'can_edit': can_edit,
      'can_approve': can_approve,
      'can_create_chapters': can_create_chapters,
      })
    return shortcuts.render_to_response(template,
                                        RequestContext(request, context))

def browse_textbooks(request):
    """View to list all the open textbooks. This view fetches tasks
    tagged with Textbook.
    """

    user = request.user


    # Get all the textbooks that are Open.
    open_textbooks = taskapp_models.Task.objects.filter(
      status=taskapp_models.TASK_STATUS_CHOICES[1][0]).order_by(
      'creation_datetime')


    context = {
      'aero_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Textbook', 'Aerospace']),
      'chemical_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Textbook', 'Chemical']),
      'computerscience_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Textbook', 'ComputerScience']),
      'electrical_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Textbook', 'Electrical']),
      'engineeringphysics_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Textbook', 'EngineeringPhysics']),
      'mechanical_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Mechanical', 'Textbook']),
      'metallurgical_textbooks': TaggedItem.objects.get_by_model(
        open_textbooks, ['Textbook', 'Metallurgical']),
      }

    # Nothing
    if user.is_authenticated() and (user.get_profile().role in
      [profile_models.ROLES_CHOICES[0][0], profile_models.ROLES_CHOICES[1][0]]):
        unpub_textbooks = taskapp_models.TextBook.objects.filter(
          status=taskapp_models.TB_STATUS_CHOICES[0][0])

        context.update({"unpub_textbooks": unpub_textbooks})

    return shortcuts.render_to_response("task/browse_textbooks.html",
                                        RequestContext(request, context))

@login_required
def edit_textbook(request, task_id):

    user = request.user
    profile = user.get_profile()

    textbook = shortcuts.get_object_or_404(taskapp_models.Task, pk=task_id)
    textbook_url = reverse(
      'view_textbook', kwargs={'task_id': textbook.id})

    if ((user == textbook.created_by or 
      user.get_profile().role != profile_models.ROLES_CHOICES[3][0])
      and textbook.status in [taskapp_models.TASK_STATUS_CHOICES[0][0],
      taskapp_models.TASK_STATUS_CHOICES[1][0]]):
        can_edit = True
    else:
        can_edit = False

    if not can_edit:
        raise exceptions.UnauthorizedAccess(NO_EDIT_RIGHT)

    context = {
      'user': user,
      'profile': profile,
      'textbook': textbook,
      }

    context.update(csrf(request))

    if request.method == "POST":
        form = taskapp_forms.EditTextbookForm(request.POST, instance=textbook)
        if form.is_valid():
            form.save()
            return shortcuts.redirect(textbook_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response(
              "task/edit.html", RequestContext(request, context))
    else:
        form = taskapp_forms.EditTextbookForm(instance=textbook)
        context.update({"form": form})
        return shortcuts.render_to_response("task/edit.html",
                                            RequestContext(request, context))

@login_required
def create_chapter(request, book_id, template='task/chapter_edit.html'):
    """View function to let Coordinators and TAs (Mentor in
    PyTask terminology) create chapters out of textbooks.

    Args:
      book_id: ID of the text book to which this chapter belongs to
    """

    user = request.user
    profile = user.get_profile()

    if profile.role != profile_models.ROLES_CHOICES[3][0]:
        can_create = True
    else:
        can_create= False

    if not can_create:
        raise http.HttpResponseForbidden

    context = {
      'user': user,
      'profile': profile,
      }

    context.update(csrf(request))

    textbook = shortcuts.get_object_or_404(taskapp_models.Task, pk=book_id)

    if request.method == 'POST':
        form = taskapp_forms.CreateChapterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()

            data.update({
              'created_by': user,
              'creation_datetime': datetime.now(),
              'parent': textbook,
              })

            # TODO: remove hard coded default publish for chapters
            data['status'] = 'Open'
            new_chapter = taskapp_models.Task(**data)
            new_chapter.save()

            textbook_url = reverse(
              'view_textbook', kwargs={'task_id': textbook.id})
            return shortcuts.redirect(textbook_url)
        else:
            context.update({"form": form})
            return shortcuts.render_to_response(
              template, RequestContext(request, context))
    else:
        form = taskapp_forms.CreateChapterForm(
          initial={'tags_field': get_intial_tags_for_chapter(textbook)})
        context.update({'form': form})
        return shortcuts.render_to_response(
          template, RequestContext(request, context))

@login_required
def edit_chapter(request, book_id, chapter_id,
                 template='task/chapter_edit.html'):
    """View function that lets edit chapters from textbooks.
    """
    chapter = shortcuts.get_object_or_404(taskapp_models.Task, pk=chapter_id)

    if chapter.parent.id != int(book_id):
        raise exceptions.PyTaskException(NOT_A_PARENT_FOR_CHAPTER)

    kwargs = {
      'task_url': reverse(
        'view_chapter', kwargs={'book_id': book_id, 'chapter_id': chapter_id})
      }

    return task_view.edit_task(request, chapter_id, **kwargs)


def view_chapter(request, book_id, chapter_id,
                 template='task/chapter_edit.html'):
    """View that displays the chapter of the textbook.

    Args:
        book_id: the id of the book to which this chapter belongs.
        chapter_id: id of the chapter that must be displayed.
    """

    chapter = shortcuts.get_object_or_404(taskapp_models.Task, pk=chapter_id)

    if chapter.parent.id != int(book_id):
        raise exceptions.PyTaskException(NOT_A_PARENT_FOR_CHAPTER)

    context = {
      'edit_url': reverse('edit_chapter', kwargs={
        'book_id': book_id, 'chapter_id': chapter_id})
      }
    kwargs = {
      'context': context,
      'task_url': reverse(
        'view_chapter', kwargs={'book_id': book_id, 'chapter_id': chapter_id})
      }

    return task_view.view_task(request, chapter_id, **kwargs)

@login_required
def approve_textbook(request, task_id):

    user = request.user
    profile = user.get_profile()

    textbook = shortcuts.get_object_or_404(taskapp_models.TextBook, pk=task_id)

    if profile.role not in [profile_models.ROLES_CHOICES[0][0], profile_models.ROLES_CHOICES[1][0]] or textbook.status != taskapp_models.TB_STATUS_CHOICES[0][0]:
        raise http.Http404

    context = {"user": user,
               "profile": profile,
               "textbook": textbook,
              }

    return shortcuts.render_to_response(
      "task/confirm_textbook_approval.html",
      RequestContext(request, context))

@login_required
def approved_textbook(request, task_id):

    user = request.user
    profile = user.get_profile()

    textbook = shortcuts.get_object_or_404(taskapp_models.TextBook, pk=task_id)

    if profile.role not in [profile_models.ROLES_CHOICES[0][0], profile_models.ROLES_CHOICES[1][0]] or textbook.status != taskapp_models.TB_STATUS_CHOICES[0][0]:
        raise http.Http404

    textbook.approved_by = user
    textbook.approval_datetime = datetime.now()
    textbook.status = taskapp_models.TB_STATUS_CHOICES[1][0]
    textbook.save()

    context = {"user": user,
               "profile": profile,
               "textbook": textbook,
              }

    return shortcuts.render_to_response(
      "task/approved_textbook.html", RequestContext(request, context))

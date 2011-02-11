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


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    ]


from urllib2 import urlparse

from django import http
from django import shortcuts
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import loader
from django.template import RequestContext
from django.utils import simplejson as json

from pytask.profile.forms import EditProfileForm
from pytask.profile.utils import get_notification
from pytask.profile.utils import get_user


@login_required
def view_profile(request, user_id=None,
                 template_name='profile/view.html'):
    """ Display the profile information of the user specified in the ID.
    """

    if user_id:
        profile_user = shortcuts.get_object_or_404(User, pk=int(user_id))
    else:
        profile_user = request.user
    profile = profile_user.get_profile()

    context = {
      'profile_user': profile_user,
      'profile': profile,
      }

    access_user_role = request.user.get_profile().role

    if (request.user == profile_user or access_user_role == 'Administrator'
      or request.user.is_superuser):
        # context variable all is used to indicate that the currently
        # logged in user has access to all the sensitive information.
        # context variable medium indicates that the currently logged
        # in user has access to medium sensitive information.
        context['all'] = True
        context['medium'] = True
    elif access_user_role == 'Coordinator':
        context['medium'] = True

    return shortcuts.render_to_response(
      template_name, RequestContext(request, context))

@login_required
def edit_profile(request):
    """ Make only a few fields editable.
    """

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }

    context.update(csrf(request))

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return shortcuts.redirect(reverse('view_profile'))
        else:
            context.update({"form":form})
            return shortcuts.render_to_response(
              "profile/edit.html", RequestContext(request, context))
    else:
        form = EditProfileForm(instance=profile)
        context.update({"form":form})
        return shortcuts.render_to_response(
          "profile/edit.html", RequestContext(request, context))

@login_required
def browse_notifications(request):
    """ get the list of notifications that are not deleted and display in
    datetime order."""

    user = request.user

    active_notifications = user.notification_sent_to.filter(
      is_deleted=False).order_by('-sent_date')

    context = {'user':user,
               'notifications':active_notifications,
              }                               

    return shortcuts.render_to_response('profile/browse_notifications.html',
                                        RequestContext(request, context))

@login_required
def view_notification(request, notification_id):
    """ get the notification depending on nid.
    Display it.
    """

    user = request.user
    newest, newer, notification, older, oldest = get_notification(
      notification_id, user)

    if not notification:
        raise http.Http404

    notification.is_read = True
    notification.save()

    context = {'user':user,
               'notification':notification,
               'newest':newest,
               'newer':newer,
               'older':older,
               'oldest':oldest,
              }

    return shortcuts.render_to_response(
      'profile/view_notification.html', RequestContext(request, context))

@login_required
def delete_notification(request, notification_id):
    """ check if the user owns the notification and delete it.
    """

    user = request.user
    newest, newer, notification, older, oldest = get_notification(
      notification_id, user)

    if not notification:
        raise http.Http404

    notification.is_deleted = True
    notification.save()

    if older:
        redirect_url = reverse('view_notification',
                               kwargs={'notification_id': older.id})
    else:
        redirect_url = reverse('browse_notifications')

    return shortcuts.redirect(redirect_url)

@login_required
def unread_notification(request, notification_id):

    """ check if the user owns the notification and delete it.
    """

    user = request.user
    newest, newer, notification, older, oldest = get_notification(
      notification_id, user)

    if not notification:
        raise http.Http404

    notification.is_read = False
    notification.save()

    if older:
        redirect_url = reverse('view_notification',
                               kwargs={'notification_id': older.id})
    else:
        redirect_url = reverse('browse_notifications')

    return shortcuts.redirect(redirect_url)

@login_required
def view_user(request, uid):

    user = request.user
    profile = user.get_profile()

    viewing_user = get_user(uid)
    viewing_profile = viewing_user.get_profile()

    working_tasks = viewing_user.approved_tasks.filter(status="Working")
    completed_tasks = viewing_user.approved_tasks.filter(status="Completed")
    reviewing_tasks = viewing_user.reviewing_tasks.all()
    claimed_tasks = viewing_user.claimed_tasks.all()

    can_view_info = True if profile.role in [
      'Administrator', 'Coordinator'] else False

    context = {"user": user,
               "profile": profile,
               "viewing_user": viewing_user,
               "viewing_profile": viewing_profile,
               "working_tasks": working_tasks,
               "completed_tasks": completed_tasks,
               "reviewing_tasks": reviewing_tasks,
               "claimed_tasks": claimed_tasks,
               "can_view_info": can_view_info,
              }

    return shortcuts.render_to_response("profile/view_user.html",
                                        RequestContext(request, context))

@login_required
def login_proceed(request):
    """View that handles the successful login.
    """

    template_name = '_user_login.html'

    # Check if the request came from logout page, if so set
    # authentication to redirect to home page
    referer_path = urlparse.urlsplit(request.META['HTTP_REFERER'])[2]
    if referer_path == reverse('auth_logout'):
      response = {
        'authentication': 'success',
        'redirect': reverse('home_page'),
        }
    elif referer_path == reverse('registration_activation_complete'):
      response = {
        'authentication': 'success',
        'redirect': reverse('view_profile'),
        }
    else:
        response = {
          'authentication': 'success',
          'markup': loader.render_to_string(template_name,
                                            RequestContext(request, {}))
        }

    json_response = json.dumps(response)
    return http.HttpResponse(json_response)

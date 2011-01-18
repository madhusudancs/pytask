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
def view_profile(request):
    """ Display the profile information.
    """

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }
    return shortcuts.render_to_response("profile/view.html",
                                        RequestContext(request, context))

@login_required
def view_user_profile(request, user_id):
    """ Display the profile information of the user specified in the ID.
    """

    user = shortcuts.get_object_or_404(User, pk=user_id)
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }
    return shortcuts.render_to_response("profile/view.html",
                                        RequestContext(request, context))

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

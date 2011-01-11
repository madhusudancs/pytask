from django.shortcuts import render_to_response, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from pytask.profile.forms import EditProfileForm
from pytask.profile.utils import get_notification, get_user

@login_required
def view_profile(request):
    """ Display the profile information.
    """

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }
    return render_to_response("profile/view.html", context)

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
            return redirect("/profile/view")
        else:
            context.update({"form":form})
            return render_to_response("profile/edit.html", context)
    else:
        form = EditProfileForm(instance=profile)
        context.update({"form":form})
        return render_to_response("profile/edit.html", context)

@login_required
def browse_notifications(request):
    """ get the list of notifications that are not deleted and display in
    datetime order."""

    user = request.user

    active_notifications = user.notification_sent_to.filter(is_deleted=False).order_by('sent_date').reverse()

    context = {'user':user,
               'notifications':active_notifications,
              }                               

    return render_to_response('profile/browse_notifications.html', context)

@login_required
def view_notification(request, nid):
    """ get the notification depending on nid.
    Display it.
    """

    user = request.user
    newest, newer, notification, older, oldest = get_notification(nid, user)

    if not notification:
        raise Http404

    notification.is_read = True
    notification.save()

    context = {'user':user,
               'notification':notification,
               'newest':newest,
               'newer':newer,
               'older':older,
               'oldest':oldest,
              }

    return render_to_response('profile/view_notification.html', context)

@login_required
def delete_notification(request, nid):
    """ check if the user owns the notification and delete it.
    """

    user = request.user
    newest, newer, notification, older, oldest = get_notification(nid, user)

    if not notification:
        raise Http404

    notification.is_deleted = True
    notification.save()

    context = {'user':user,
               'notification':notification,
               'newest':newest,
               'newer':newer,
               'older':older,
               'oldest':oldest,
              }

    if older:
        redirect_url = "/profile/notf/view/nid=%s"%older.uniq_key
    else:
        redirect_url = "/profile/notf/browse"

    return redirect(redirect_url)

@login_required
def unread_notification(request, nid):

    """ check if the user owns the notification and delete it.
    """

    user = request.user
    newest, newer, notification, older, oldest = get_notification(nid, user)

    if not notification:
        raise Http404

    notification.is_read = False
    notification.save()

    context = {'user':user,
               'notification':notification,
               'newest':newest,
               'newer':newer,
               'older':older,
               'oldest':oldest,
              }

    if older:
        redirect_url = "/profile/notf/view/nid=%s"%older.uniq_key
    else:
        redirect_url = "/profile/notf/browse"

    return redirect(redirect_url)

@login_required
def view_user(request, uid):

    user = request.user
    profile = user.get_profile()

    viewing_user = get_user(uid)
    viewing_profile = viewing_user.get_profile()

    working_tasks = viewing_user.approved_tasks.filter(status="WR")
    completed_tasks = viewing_user.approved_tasks.filter(status="CM")
    reviewing_tasks = viewing_user.reviewing_tasks.all()
    claimed_tasks = viewing_user.claimed_tasks.all()

    can_view_info = True if profile.rights in ["MG", "DC"] else False

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

    return render_to_response("profile/view_user.html", context)

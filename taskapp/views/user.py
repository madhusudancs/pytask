import os

from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from pytask.taskapp.models import Task, Profile, Request

from pytask.taskapp.events.user import createUser
from pytask.taskapp.events.request import reply_to_request

from pytask.taskapp.forms.user import UserProfileEditForm, UserChoiceForm

from pytask.taskapp.utilities.request import get_request, create_request
from pytask.taskapp.utilities.notification import get_notification, create_notification
from pytask.taskapp.utilities.user import get_user

about = {
    "addreviewers": "about/addreviewers.html",
    "reviewer": "about/reviewer.html", 
    "starthere": "about/starthere.html",
    "task": "about/task.html",
    "tasklife": "about/tasklife.html",
    "developer": "about/developer.html",
    "notification": "about/notification.html",
    "request": "about/request.html",
    "manager": "about/manager.html",
    "admin": "about/admin.html",
}

def show_msg(user, message, redirect_url=None, url_desc=None):
    """ simply redirect to homepage """
    
    return render_to_response('show_msg.html',{'user':user, 'message':message, 'redirect_url':redirect_url, 'url_desc':url_desc})

def homepage(request):
    """ check for authentication and display accordingly. """
   
    user = request.user
    is_guest = False
    is_reviewer = False
    can_create_task = False
    task_list = []
    
    if not user.is_authenticated():
        is_guest = True
        disp_num = 10
        task_list = Task.objects.exclude(status="UP").exclude(status="CD").exclude(status="CM").order_by('published_datetime').reverse()[:10]
        return render_to_response('index.html', {'user':user, 'is_guest':is_guest, 'task_list':task_list})
        
    else:
        user = get_user(request.user)
        user_profile = user.get_profile()
        is_reviewer = True if user.task_reviewers.all() else False
        can_create_task = False if user_profile.rights == u"CT" else True
        
        context = {'user':user,
                   'is_guest':is_guest,
                   'is_reviewer':is_reviewer,
                   'task_list':task_list,
                   'can_create_task':can_create_task,
                   }

        context["unpublished_tasks"] = user.task_reviewers.filter(status="UP")
        context["reviewered_tasks"] = user.task_reviewers.exclude(status="UP").exclude(status="CM").exclude(status="CD").exclude(status="DL")
        context["claimed_tasks"] = user.task_claimed_users.exclude(status="UP").exclude(status="CM").exclude(status="CD").exclude(status="DL")
        context["working_tasks"] = user.task_assigned_users.filter(status="WR")
                   
        return render_to_response('index.html', context)

@login_required
def learn_more(request, what):
    """ depending on what was asked for, we render different pages.
    """

    user = get_user(request.user)
    disp_template = about.get(what, None)
    if not disp_template:
        raise Http404
    else:
        return render_to_response(disp_template, {'user':user})

@login_required
def view_my_profile(request,uid=None):
    """ allows the user to view the profiles of users """
    user = get_user(request.user)
    request_user_profile = request.user.get_profile()
    request_user_privilege = True if request_user_profile.rights in ['AD','MG'] else False
    if uid == None:
        edit_profile = True
        profile = Profile.objects.get(user = request.user)
        return render_to_response('user/my_profile.html', {'edit_profile':edit_profile,'profile':profile, 'user':user, 'privilege':request_user_privilege})
    edit_profile = True if request.user == User.objects.get(pk=uid) else False
    try:
        profile = Profile.objects.get(user = User.objects.get(pk=uid))
    except Profile.DoesNotExist:
        raise Http404
    return render_to_response('user/my_profile.html', {'edit_profile':edit_profile,'profile':profile, 'user':user, 'privilege':request_user_privilege})

@login_required
def edit_my_profile(request):
    """ enables the user to edit his/her user profile """

    user = get_user(request.user)
    user_profile = user.get_profile()

    edit_profile_form = UserProfileEditForm(instance = user_profile)
    if request.method == 'POST':

        data = request.POST.copy()
        uploaded_photo = request.FILES.get('photo', None)
        data.__setitem__('photo', uploaded_photo)

        edit_profile_form = UserProfileEditForm(data, instance=user_profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            return redirect('/user/view/uid='+str(user.id))
        else:
            return render_to_response('user/edit_profile.html',{'user':user, 'edit_profile_form' : edit_profile_form})
    else:
        profile = user.get_profile()
        edit_profile_form = UserProfileEditForm(instance = profile)
        return render_to_response('user/edit_profile.html',{'edit_profile_form' : edit_profile_form, 'user':user})

@login_required
def browse_requests(request):
    
    user = get_user(request.user)
    active_reqs = user.request_sent_to.filter(is_replied=False).exclude(is_valid=False)
    reqs = active_reqs.order_by('creation_date').reverse()

    context = {
        'user':user,
        'reqs':reqs,
    }

    return render_to_response('user/browse_requests.html', context)

@login_required
def view_request(request, rid):
    """ please note that request variable in this method is that of django.
    our app request is called user_request.
    """

    user = get_user(request.user)
    user_rights = user.get_profile().rights
    newest, newer, user_request, older, oldest = get_request(rid, user)
    if not user_request:
        raise Http404

    user_request.is_read = True
    user_request.save()

    context = {
        'user':user,
        'req':user_request,
        'sent_users':user_request.sent_to.all(),
        'newest':newest,
        'newer':newer,
        'older':older,
        'oldest':oldest,
    }

    return render_to_response('user/view_request.html', context)

@login_required
def process_request(request, rid, reply):
    """ check if the method is post and then update the request.
    if it is get, display a 404 error.
    """

    user = get_user(request.user)
    browse_request_url= '/user/requests'
    newest, newer, req_obj, older, oldest = get_request(rid, user)

    if not req_obj:
        return show_msg(user, "Your reply has been processed", browse_request_url, "view other requests")

    if request.method=="POST":
        reply = True if reply == "yes" else False
        req_obj.remarks = request.POST.get('remarks', "")
        req_obj.save()

        reply_to_request(req_obj, reply, user)

        return redirect('/user/requests/')
        return show_msg(user, "Your reply has been processed", browse_request_url, "view other requests")
    else:
        return show_msg(user, "You are not authorised to do this", browse_request_url, "view other requests")

@login_required
def browse_notifications(request):
    """ get the list of notifications that are not deleted and display in datetime order.
    """

    user = get_user(request.user)

    active_notifications = user.notification_sent_to.filter(is_deleted=False).order_by('sent_date').reverse()

    context = {
        'user':user,
        'notifications':active_notifications,
    }

    return render_to_response('user/browse_notifications.html', context)

@login_required
def view_notification(request, nid):
    """ get the notification depending on nid.
    Display it.
    """

    user = get_user(request.user)
    newest, newer, notification, older, oldest = get_notification(nid, user)
    if not notification:
        raise Http404

    notification.is_read = True
    notification.save()

    context = {
        'user':user,
        'notification':notification,
        'newest':newest,
        'newer':newer,
        'older':older,
        'oldest':oldest,
    }

    return render_to_response('user/view_notification.html', context)

@login_required
def edit_notification(request, nid, action):
    """ if action is delete, set is_deleted.
    if it is unread, unset is_read.
    save the notification and redirect to browse_notifications.
    """

    user = get_user(request.user)
    newest, newer, notification, older, oldest = get_notification(nid, user)

    if not notification:
        raise Http404

    notifications_url = "/user/notifications/"

    if request.method == "POST":
        if action == "delete":
            notification.is_deleted = True
        elif action == "unread":
            notification.is_read = False
        
        notification.save()
        if older:
            return redirect('/user/notifications/nid=%s'%older.id)
        else:
            return redirect(notifications_url)
    else:
        return show_msg(user, 'This is wrong', notification_url, "view the notification")
 
@login_required
def change_rights(request, role):
    """ check if the current user has privileges to do this.
    """
    
    user = get_user(request.user)
    role = role.upper()
    user_profile = user.get_profile()
    user_rights = user_profile.rights

    user_can_view = True if user_rights == "AD" or ( user_rights == "MG" and role in ["MG", "DV"] ) else False

    if user_can_view:
        if role == "DV":
            current_contributors = list(User.objects.filter(is_active=True,profile__rights="CT"))
            pending_requests = user.request_sent_by.filter(is_replied=False,is_valid=True)
            pending_dv_requests = pending_requests.filter(role="DV")

            ## one cannot make same request many times
            for req in pending_dv_requests:
                current_contributors.remove(req.sent_to.all()[0])

            choices = [ (_.id,_.username ) for _ in current_contributors ]

        elif role == "MG":
            active_users = User.objects.filter(is_active=True)
            dv_ct_users = list(active_users.filter(profile__rights="CT") | active_users.filter(profile__rights="DV"))
            pending_requests = user.request_sent_by.filter(is_replied=False,is_valid=True)
            pending_mg_requests = pending_requests.filter(role="MG")

            ## same logic here. you cannot make another request exactly the same.
            ## but iam still not decided whether someone who requests a user to be admin,
            ## can be given a chance to request the same user to be a manager or developer
            for req in pending_mg_requests:
                dv_ct_users.remove(req.sent_to.all()[0])

            choices = [ (_.id, _.username ) for _ in dv_ct_users ]

        elif role == "AD":
            active_users = User.objects.filter(is_active=True)
            non_ad_users = list(active_users.exclude(profile__rights="AD"))
            pending_requests = user.request_sent_by.filter(is_replied=False,is_valid=True)
            pending_ad_requests = pending_requests.filter(role="AD")

            ## we filter out users who have already been requested by the user to be an admin
            for req in pending_ad_requests:
                non_ad_users.remove(req.sent_to.all()[0])

            choices = [ (_.id,_.username ) for _ in non_ad_users ]

        form = UserChoiceForm(choices)

        context = {
            'user':user,
            'form':form,
        }

        if request.method=="POST":
            data = request.POST
            form = UserChoiceForm(choices, data)
            if form.is_valid():
                user_to_change = User.objects.get(id=form.cleaned_data['user'])
                create_request(sent_by=user, role=role, sent_to=user_to_change)
                return show_msg(user, "A request has been sent", "/", "return to home page")
            else:
                raise Http404
        else:
            return render_to_response('user/changerole.html', context)
    else:
        raise Http404

















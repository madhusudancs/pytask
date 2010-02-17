from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render_to_response
from pytask.taskapp.models import Task
from pytask.taskapp.forms.user import UserProfileEditForm
from pytask.taskapp.events.user import createUser, updateProfile
from django.contrib.auth.models import User
from pytask.taskapp.models import Profile
from django.contrib.auth.decorators import login_required


def show_msg(message, redirect_url=None, url_desc=None):
    """ simply redirect to homepage """
    
    return render_to_response('show_msg.html',{'message':message, 'redirect_url':redirect_url, 'url_desc':url_desc})

def homepage(request):
    """ check for authentication and display accordingly. """
    
    user = request.user
    is_guest = False
    is_mentor = False
    can_create_task = False
    task_list = []
    
    if not user.is_authenticated():
        is_guest = True
        disp_num = 10
        tasks_count = Task.objects.count()
        if tasks_count <= disp_num:
            task_list = Task.objects.order_by('id').reverse()
        else:
            task_list = Task.objects.order_by('id').reverse()[:10]
            
        return render_to_response('index.html', {'is_guest':is_guest, 'task_list':task_list})
        
    else:
        user_profile = user.get_profile()
        is_mentor = True if user.task_mentors.all() else False
        can_create_task = False if user_profile.rights == u"CT" else True
        
        context = {'user':user,
                   'is_guest':is_guest,
                   'is_mentor':is_mentor,
                   'task_list':task_list,
                   'can_create_task':can_create_task,
                   }
                   
        return render_to_response('index.html', context)

@login_required
def view_my_profile(request,uid=None):
    """ allows the user to view the profiles of users """
    if uid == None:
        edit_profile = True
        profile = Profile.objects.get(user = request.user)
        return render_to_response('user/my_profile.html', {'edit_profile':edit_profile,'profile':profile})
    edit_profile = True if request.user == User.objects.get(pk=uid) else False
    try:
        profile = Profile.objects.get(user = User.objects.get(pk=uid))
    except Profile.DoesNotExist:
        raise Http404
    return render_to_response('user/my_profile.html', {'edit_profile':edit_profile,'profile':profile})

def edit_my_profile(request):
    """ enables the user to edit his/her user profile """
    if str(request.user) == 'AnonymousUser':
        return show_msg('Please register yourself to activate the functionality')
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST)
#        if not form.is_valid():
#            edit_profile_form = UserProfileEditForm(instance = form)
#            return render_to_response('user/edit_profile.html',{'edit_profile_form' : edit_profile_form})
        if request.user.is_authenticated() == True:
            profile = Profile.objects.get(user = request.user)
            data = request.POST#form.cleaned_data
            properties = {'aboutme':data['aboutme'], 'foss_comm':data['foss_comm'], 'phonenum':data['phonenum'], 'homepage':data['homepage'], 'street':data['street'], 'city':data['city'], 'country':data['country'], 'nick':data['nick']}
            #fields = ['dob','gender','credits','aboutme','foss_comm','phonenum','homepage','street','city','country','nick']
            updateProfile(profile,properties)
            return redirect('/user/view/uid='+str(profile.user_id))
    else:
        profile = Profile.objects.get(user = request.user)
        edit_profile_form = UserProfileEditForm(instance = profile)
        return render_to_response('user/edit_profile.html',{'edit_profile_form' : edit_profile_form})


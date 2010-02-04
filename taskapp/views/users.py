from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from pytask.taskapp.models import Task
from pytask.taskapp.forms.user import RegistrationForm, LoginForm
from pytask.taskapp.events.user import createUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def redirect_to_homepage(request):
    """ simply redirect to homepage """
    
    return redirect('/')

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


def register(request):
    """ user registration: gets the user details and create the user and userprofile if data entered is valid"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == data['repeat_password']:
                try:
                    if User.objects.get(username__exact = data['username']):
                        errors=['Choose some other username']
                        return render_to_response('user/register.html',{'form':form,'errors':errors})
                except:
                     u = createUser(username=data['username'], email=data['email'], password=data['password'],dob = data['dob'],gender = data['gender'])
                return redirect('/accounts/login/')
            else:
                errors=['Password do not match']
                form = RegistrationForm(request.POST)
                return render_to_response('user/register.html',{'form':form,'errors':errors})#HttpResponse('Password did not match')
        else:
            form = RegistrationForm()
    else:
        form = RegistrationForm()
    return render_to_response('user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')# Redirect to a success page.
            else:
                return HttpResponse('username is not active, please contact the administrator')# Return a 'disabled account' error message
        else:
            errors = ['Please check your username and password']
            form = LoginForm()
            return render_to_response('user/login.html',{'form':form,'errors':errors})# Return an 'invalid login' error message.
        return redirect('/')
    else:
        form = LoginForm()
        return render_to_response('user/login.html',{'form': form})

def user_logout(request):
    logout(request)
    return HttpResponse('You have logged off successfully!!!')

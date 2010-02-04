from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from pytask.taskapp.models import Task

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
               


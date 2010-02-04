from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from pytask.taskapp.models import Task, Comment
from pytask.taskapp.forms.task import TaskCreateForm
from pytask.taskapp.events.task import createTask, addMentor, publishTask
from pytask.taskapp.views.user import show_msg

def browse_tasks(request):
    """ display all the tasks """
    
    user = request.user
    task_list = Task.objects.order_by('id').reverse()
    
    context = {'user':user,
               'task_list':task_list,
               }
    return render_to_response('task/browse.html', context)

def view_task(request, tid):
    """ get the task depending on its tid and display accordingly if it is a get.
    check for authentication and add a comment if it is a post request.
    """
    
    task_url = "/task/view/tid=%s"%tid
    
    user = request.user
    task = Task.objects.get(id=tid)
    comments = Comment.objects.filter(task=task)
    errors = []
    
    is_guest = True if not user.is_authenticated() else False
    is_mentor = True if user in task.mentors.all() else False
    
    context = {'user':user,
               'task':task,
               'comments':comments,
               'is_guest':is_guest,
               'is_mentor':is_mentor,
               'errors':errors,
               }
    
    if request.method == 'POST':
        if not is_guest:
            data = request.POST["data"]
            task = Task.objects.get(id=tid)
            new_comment = Comment(task=task, data=data, created_by=user, creation_datetime=datetime.now())
            new_comment.save()
            return redirect(task_url)
        else:
            errors.append("You must be logged in to post a comment")
            return render_to_response('task/view.html', context)
    else:
        return render_to_response('task/view.html', context)
        
def create_task(request):
    """ check for rights and create a task if applicable.
    if user cannot create a task, redirect to homepage.
    """
    
    user = request.user
    is_guest = True if not user.is_authenticated() else False
    
    if not is_guest:
        user_profile = user.get_profile()
        can_create_task = False if user_profile.rights == "CT" else True
        if can_create_task:
            if request.method == "POST":
                form = TaskCreateForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    title = data['title']
                    desc = data['desc']
                    credits = data['credits']
                    publish = data['publish']
                    task = createTask(title,desc,user,credits)
                    
                    if not task:
                        error_msg = "Another task with the same title exists"
                        return render_to_response('task/create.html',{'form':form, 'error_msg':error_msg})
                    
                    addMentor(task, user)
                    if publish: publishTask(task)    
                    task_url = '/task/view/tid=%s'%task.id
                    return redirect(task_url)
                else:
                    return render_to_response('task/create.html',{'form':form})
            else:
                form = TaskCreateForm()
                return render_to_response('task/create.html',{'form':form})
        else:
            return show_msg('You are not authorised to create a task.')
    else:
        return show_msg('You are not authorised to create a task.')
    
    
    
    
    
    
    
    
    
    
    
    
    
    

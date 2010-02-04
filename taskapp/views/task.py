from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from pytask.taskapp.models import Task, Comment

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

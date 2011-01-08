from datetime import datetime

from django.shortcuts import render_to_response, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from pytask.utils import make_key
from pytask.views import show_msg

from pytask.taskapp.models import Task
from pytask.taskapp.forms import CreateTaskForm, EditTaskForm
from pytask.profile.utils import get_notification


@login_required
def create_task(request):

    user = request.user
    profile = user.get_profile()

    context = {"user": user,
               "profile": profile,
              }

    context.update(csrf(request))

    can_create_task = False if user_profile.rights == "CT" else True
    if can_create_task:
        if request.method == "POST":
            form = TaskCreateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data.copy()
                data.update({"created_by": user,
                             "creation_datetime": datetime.now(),
                             "uniq_key": make_key(Task),
                            })
                
                task = Task(**data)
                task.save()

                task_url = '/task/view/tid=%s'%task.uniq_key
                return redirect(task_url)
            else:
                return render_to_response('task/create.html',{'user':user, 'form':form})
        else:
            form = TaskCreateForm()
            return render_to_response('task/create.html',{'user':user, 'form':form})
    else:
        return show_msg(user, 'You are not authorised to create a task.')

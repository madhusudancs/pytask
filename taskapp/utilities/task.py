from django.http import Http404
from pytask.taskapp.models import Task, Map

def getTask(tid):
    """ retreive the task from database.
    if the task has deps or subs, update its status correspondingly.
    """

    try:
        task = Task.objects.get(id=tid)
    except Task.DoesNotExist:
        raise Http404
    try:
        mapobj = Map.objects.get(main=task)
    except Map.DoesNotExist:
        mapobj = Map()
        mapobj.main = task
        mapobj.save()
        
    task_subs = mapobj.subs.all()

    if task.sub_type == "D":
        task.deps, task.subs = task_subs, []
    elif task.sub_type == "S":
        task.subs, task.deps = task_subs, []

    deps, subs = task.deps, task.subs
    if deps and task.status in ["OP", "LO"]:
        task.status = "OP" if all(map(lambda t:t.status=="CM",deps)) else "LO"

    ## a task with subs will remain in "LO" and will be made "OP" only if all subs are removed.
    if subs and task.status in ["OP", "LO"]:
        task.status = "LO"

    task.save()
    return task


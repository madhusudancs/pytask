from pytask.taskapp.models import Task, TextBook
from django.http import Http404

def getTask(tid):

    try:
        task = Task.objects.get(uniq_key=tid)
        return task
    except Task.DoesNotExist:
        raise Http404

def getTextBook(tid):

    try:
        task = TextBook.objects.get(uniq_key=tid)
        return task
    except TextBook.DoesNotExist:
        raise Http404


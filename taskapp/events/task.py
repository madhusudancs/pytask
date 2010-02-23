from datetime import datetime
from pytask.taskapp.models import Profile, Task, Comment, Credit, Claim

def publishTask(task):
    """ set the task status to open """
    
    sub_tasks = task.subs.all()
    dependencies = task.deps.all()
    if sub_tasks or any(map(lambda t:t.status!="CM",dependencies)):
        task.status = "LO"
    else:
        task.status = "OP"
    task.save()
    return task

def addMentor(task,mentor):
    """ add the mentor to mentors list of the task """
    
    task.mentors.add(mentor)
    task.save()
    return task    
    
def createTask(title,desc,created_by,credits):
    """ creates a bare minimum task with title, description and credits.
    the creator of the task will be assigned as a mentor for the task.
    """

    try:
        task = Task.objects.get(title__iexact=title)
        return None
    except Task.DoesNotExist:
        task = Task(title=title)
    task.desc = desc
    task.created_by = created_by
    task.credits = credits
    task.creation_datetime = datetime.now()
    task.save()
    return task

def addSubTask(main_task, sub_task):
    """ add sub_task to subs list of main_task """
    
    main_task.subs.add(sub_task)
    main_task.status = "LO"
    main_task.save()
    return main_task

def addClaim(task, message, user):
    """ add claim data to the database if it does not exist 
    and also update the claimed users field of the task.
    """
    
    task.claimed_users.add(user)
    task.status = "CL"
    task.save()
    claim = Claim()
    claim.message = message
    claim.task = task
    claim.user = user
    claim.creation_datetime = datetime.now()
    claim.save()
    
def assignTask(task, user):
    """ check for the status of task and assign it to the particular user """
    
    task.assigned_users.add(user)
    task.status = "AS"
    task.save()

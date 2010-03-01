from datetime import datetime
from pytask.taskapp.models import Profile, Task, Comment, Claim, Map
from pytask.taskapp.utilities.task import getTask
from pytask.taskapp.utilities.request import create_request
from pytask.taskapp.utilities.helper import get_key
from pytask.taskapp.utilities.notification import create_notification

def publishTask(task, rem_mentors=True, rem_comments=True):
    """ set the task status to open """

    if task.sub_type == 'D':
        deps, subs = task.map_subs.all(), []
    else:
        subs, deps = task.map_subs.all(), []
   
    if subs or any(map(lambda t:t.status!="CM",deps)):
        task.status = "LO"
    else:
        task.status = "OP"

    if rem_mentors:
        task.mentors.clear()
        task.mentors.add(task.created_by)

    if rem_comments:
        task.comment_set.update(is_deleted=True)
        task.comment_set.update(deleted_by=task.created_by)

    task.published_datetime = datetime.now()
    task.save()

    pending_requests = task.request_task.filter(is_valid=True, is_replied=False)
    pending_requests.update(is_valid=False)

    return task

def addSubTask(main_task, sub_task):
    """ add the task to subs attribute of the task and update its status.
    sub task can be added only if a task is in UP/OP/LO state.
    """

    ## Shall modify after talking to pr about subtasks
    ## I think i might even remove the concept of subtasks

    main_task.sub_type = "S"
    main_task.save()

    try:
        mapobj = Map.objects.get(main=main_task)
    except Map.DoesNotExist:
        mapobj = Map()
        mapobj.main = main_task
        mapobj.save()
    mapobj.subs.add(sub_task)
    mapobj.save()

    sub_tasks = getTask(main_task.id).subs
    if main_task.status == "OP":
        if any(map(lambda t:t.status!="CM",sub_tasks)):
            main_task.status = "LO"
        else:
            "CM"
    main_task.save()

def addDep(main_task, dependency):
    """ add the dependency task to deps attribute of the task.
    update the status of main_task accordingly.
    note that deps can be added only if task is in UP/OP/LO state.
    And also if the task doesn't have any subs.
    """

    main_task.sub_type = "D"
    main_task.save()

    try:
        mapobj = Map.objects.get(main=main_task)
    except Map.DoesNotExist:
        mapobj = Map()
        mapobj.main = main_task
        mapobj.save()

    mapobj.subs.add(dependency)
    mapobj.save()

    deps = getTask(main_task.id).deps

    if main_task.status in ["OP", "LO"]: 
        if all(map(lambda t:t.status=="CM",deps)):
            main_task.status = "OP"
        else:
            main_task.status = "LO"
    
    main_task.save()

def reqMentor(task, mentor, req_by):
    """ create a request object with role as MT.
    """

    create_request(sent_by=req_by, role="MT", sent_to=mentor, task=task) 

def addMentor(task,mentor):
    """ add the mentor to mentors list of the task """
    
    task.mentors.add(mentor)
    task.save()
    return task     

def createTask(title,desc,created_by,credits):
    """ creates a bare minimum task with title, description and credits.
    the creator of the task will be assigned as a mentor for the task.
    """

    while True:
        id = get_key()
        try:
            task = Task.objects.get(id__iexact=id)
            continue
        except Task.DoesNotExist:
            break

    try:
        task = Task.objects.get(title__iexact=title)
        return None
    except:
        task = Task(title=title)

    task.id = id 
    task.desc = desc
    task.created_by = created_by
    task.credits = credits
    task.creation_datetime = datetime.now()
    task.published_datetime = datetime.now()
    task.save()
    return task

def addClaim(task, message, user):
    """ add claim data to the database if it does not exist 
    and also update the claimed users field of the task.
    """
    
    task.claimed_users.add(user)
    task.save()
    claim = Claim()
    claim.message = message
    claim.task = task
    claim.user = user
    claim.creation_datetime = datetime.now()
    claim.save()

    user.request_sent_to.filter(is_replied=False, is_valid=True, role="MT", task=task).update(is_valid=False)
    
def assignTask(task, added_user, assigned_by):
    """ check for the status of task and assign it to the particular user """
    
    if task.status in ['OP', 'WR']:
        task.assigned_users.add(added_user)
        task.claimed_users.remove(added_user)
        task.status = "WR"
    task.save()

    create_notification("AU", added_user, assigned_by, task=task)


def updateTask(task, title=None, desc=None, credits=None, tags_field=None):
    """ update the property accordingly.
    while updating title, check for uniqueness of title.
    return None if any error. 
    """
    
    if title:
        try:
            task.title = title
            task.save()
        except Task.IntegrityError:
            return None
    if desc:task.desc = desc
    if credits:task.credits = credits
    if tags_field:task.tags_field = tags_field
    task.save()
    return task

def removeTask(main_task, sub_task):
    """ get the corresponding map object and remove the sub_task.
    """

    mapobj = Map.objects.get(main=main_task)
    mapobj.subs.remove(sub_task)
    mapobj.save()

def removeUser(main_task, rem_user, removed_by, reason=None):
    """ right now, just remove the user from the list of assigned_users.
    """

    main_task.assigned_users.remove(rem_user)
    main_task.save()

    ## TODiscuss : when a user is kicked off, his pending requests for pynts is made invalid
    rem_user.request_receiving_user.filter(task=main_task,role="PY",is_valid=True,is_replied=False).update(is_valid=False)

    create_notification("RU", rem_user, removed_by, task=main_task, remarks=reason)
    ## TODO : create notification to the victim

def assignCredits(task, given_by, given_to, points):
    """ make a proper request object.
    """
    
    create_request(sent_by=given_by, role="PY", task=task, receiving_user=given_to, pynts=points ) 

def completeTask(task, marked_by):
    """ set the status of task as completed.
    We dont have to inform parent tasks.
    That part is taken care by getTask method.
    """

    task.status = "CM"
    task.save()

    pending_requests = task.request_task.filter(is_replied=False)
    pending_requests.update(is_valid=False)

    ## generate notification appropriately using marked_by
    ## we also have to mark unread requests as invalid

    for a_user in task.assigned_users.all():
        create_notification(role="CM", sent_to=a_user, sent_from=marked_by, task=task)

    for a_user in task.claimed_users.all():
        create_notification(role="CM", sent_to=a_user, sent_from=marked_by, task=task)

    for a_mentor in task.mentors.all():
        create_notification(role="CM", sent_to=a_mentor, sent_from=marked_by, task=task)



def closeTask(task, closed_by, reason=None):
    """ set the status of task as CD.
    generate notifications accordingly.
    """

    task.status = "CD"
    task.save()

    pending_requests = task.request_task.filter(is_replied=False)
    pending_requests.update(is_valid=False)

    ## generate notifications here

    for a_user in task.assigned_users.all():
        create_notification(role="CD", sent_to=a_user, sent_from=closed_by, task=task, remarks=reason)

    for a_user in task.claimed_users.all():
        create_notification(role="CD", sent_to=a_user, sent_from=closed_by, task=task, remarks=reason)

    for a_mentor in task.mentors.all():
        create_notification(role="CD", sent_to=a_mentor, sent_from=closed_by, task=task, remarks=reason)



from pytask.taskapp.models import Request
from datetime import datetime

def create_request(to,by,role,task=None,assigned_user=None):
    """
    creates an unreplied request, based on the passed arguments
        to - a list of users to which the notification is to be sent
        by - sender of request
        role - a two character field which represents the role requested
        task - a requesting task (useful for sending admins a request to give Pynts to the user)
        assigned_user - user to whom the Pynts/Task is assigned to(useful for sending admins a request to give Pynts to the user)
    """
    req = Request(creation_date=datetime.now())
    req.by = by
    req.reply_date = datetime(1970,01,01)
    req.save()
    req.to = to
    req.role = role
    if task:
        req.task = task
    if assigned_user:
        req.assigned_user = assigned_user
    req.save()

def reply_to_request(request_id, reply):
    """
    makes a request replied with the given reply.
    arguments:
        request_id - a number denoting the id of the Request object
        reply - a boolean value to be given as reply (True/False)
    """
    try:
        request = Request.objects.get(id = request_id)
    except Request.DoesNotExist:
        return False #No such request exist
    if not request.replied:
        request.reply = reply
        request.replied = True
        request.read = True
        request.reply_date = datetime.now()
        request.save()
        return True #Reply has been added successfully
    return False #Already replied

from pytask.taskapp.models import Request
from datetime import datetime

def create_request(to,by,role,task=None,assigned_user=None):
    """
    creates an unreplied request, based on the passed arguments
        to - a list of users to which the notification is to be sent
        by - sender of request
        role - a two character field which represents the role requested
        task - a requesting task (useful for sending admins a request to give Pynts to the user, assigning a user to a task)
        assigned_user - user to whom the Pynts/Task is assigned to(useful for sending admins a request to give Pynts to the user, assigning a user to a task)
    """
    req = Request(creation_date=datetime.now())
    req.by = by
    req.reply_date = datetime(1970,01,01)
    req.save()
    req.to = to
    req.role = role
    if task not None:
        req.task = task
    if assigned_user not None:
        req.assigned_user = assigned_user
    req.save()

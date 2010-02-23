from pytask.taskapp.models import Request
from datetime import datetime

def create_request(to,by,role):
    """
    creates an unreplied request, based on the passed arguments
        to - a list of users to which the notification is to be sent
        by - sender of request
        role - a two character field which represents the role requested
    """
    req = Request(creation_date=datetime.now())
    req.by = by
    req.reply_date = datetime(1970,01,01)
    req.save()
    req.to = to
    req.role = role
    req.save()

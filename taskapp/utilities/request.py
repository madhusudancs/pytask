from pytask.taskapp.models import Request, Profile
from datetime import datetime
from django.contrib.auth.models import User

def create_request(sent_by,role,sent_to=None,task=None,receiving_user=None,pynts=0):
    """
    creates an unreplied request, based on the passed arguments
        sent_to - a list of users to which the notification is to be sent
        sent_by - sender of request
        role - a two character field which represents the role requested, if role = 'PY' then sent to all admins
        task - a requesting task (useful for sending admins a request to give Pynts to the user)
        receiving_user - user to whom the Pynts is assigned to(useful for sending admins a request to give Pynts to the user)
        pynts - the pynts assigned to the receiving user
    """
    req = Request(creation_date=datetime.now())
    req.sent_by = sent_by
    req.reply_date = datetime(1970,01,01)
    req.role = role
    req.pynts = pynts
    if task:
        req.task = task
    req.save()
    if role == 'PY':
        admin_profiles = Profile.objects.filter(rights='AD')
        for admin in admin_profiles:
            req.sent_to.add(admin_profile.user)
        req.receiving_user = receiving_user
    else:
        req.sent_to.add(sent_to)
    req.save()

def reply_to_request(request_obj, reply, replied_by):
    """
    makes a request replied with the given reply.
    arguments:
        request_obj - Request object for which change is intended
        reply - a boolean value to be given as reply (True/False)
        replied_by - the user object who replies to the request
    """
    if not request_obj.is_replied:
        request_obj.reply = reply
        request_obj.is_replied = True
        request_obj.is_read = True
        request_obj.reply_date = datetime.now()
        request_obj.replied_by = replied_by
        request_obj.save()
        return True #Reply has been added successfully
    return False #Already replied

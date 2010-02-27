from datetime import datetime

from django.contrib.auth.models import User
from pytask.taskapp.models import Request, Profile

def create_request(sent_by,role,sent_to=None,task=None,receiving_user=None,pynts=0):
    """
    creates an unreplied request, based on the passed arguments
        sent_to - a list of users to which the request is to be sent
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
        for admin_profile in admin_profiles:
            req.sent_to.add(admin_profile.user)
        req.receiving_user = receiving_user
    else:
        req.sent_to.add(sent_to)
    req.save()

def get_request(rid, user):
    """ see if the request is replied or if he can not view the request,
    raise 404 error. else return request.
    """

    try:
        request_obj = Request.objects.get(id=rid)
    except Request.DoesNotExist:
        return None

    if request_obj.is_replied == True:
        return None
    else:
        try:
            request_obj.sent_to.get(id=user.id)
        except User.DoesNotExist:
            return None
        return request_obj

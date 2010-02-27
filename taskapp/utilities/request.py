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

    active_requests = user.request_sent_to.filter(is_valid=True, is_replied=False).order_by('creation_date')
    current_requests = active_requests.filter(id=rid)
    if current_requests:
        current_request = current_requests[0]

        try:
            newer_request = current_request.get_next_by_creation_date(sent_to=user, is_replied=False, is_valid=True)
            newest_request = active_requests.reverse()[0]
            if newer_request == newest_request:
                newest_request = None
        except Request.DoesNotExist:
            newer_request, newest_request = None, None

        try:
            older_request = current_request.get_previous_by_creation_date(sent_to=user, is_replied=False, is_valid=True)
            oldest_request = active_requests[0]
            if oldest_request == older_request:
                oldest_request = None
        except Request.DoesNotExist:
            older_request, oldest_request = None, None

        return newest_request, newer_request, current_request, older_request, oldest_request 

    else:
        return None, None, None, None, None

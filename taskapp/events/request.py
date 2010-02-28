from datetime import datetime
from pytask.taskapp.models import Profile
from pytask.taskapp.events.task import addCredits, addMentor
from pytask.taskapp.events.user import changeRole
from pytask.taskapp.utilities.notification import create_notification

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
        request_obj.reply_date = datetime.now()
        request_obj.replied_by = replied_by
        request_obj.save()

        if request_obj.role == "PY":
            ## note that we are not doing any check. we make requests invalid when an event like closing task happens.
            task = request_obj.task
            pynts = request_obj.pynts
            receiving_user = request_obj.receiving_user
            requested_by = request_obj.sent_by
            for a_mentor in task.mentors.all():
                if reply:
                    addCredits(task, request_obj.sent_by, request_obj.receiving_user, pynts)
                    create_notification(request_obj.role, a_mentor, replied_by, True, task, request_obj.remarks, requested_by, receiving_user, pynts)
                else:
                    create_notification(request_obj.role, a_mentor, replied_by, False, task, request_obj.remarks, requested_by, receiving_user, pynts)

        elif request_obj.role == "MT":
            task = request_obj.task
            requested_by = request_obj.sent_by
            if reply:
                ## tell the replied user that he is mentor for this task and give him learn more link
                create_notification("NT", request_obj.replied_by, task=task) 

                ## now check if there are such similar requests and mark them as invalid
                ## they cannot be of type PY and so we can use the replied_by to get requests
                pending_requests = replied_by.request_sent_to.filter(is_valid=True, is_replied=False, role="MT",task=task)
                for req in pending_requests:
                       create_notification("MT", req.sent_by, replied_by, False, task=req.task, remarks = "User has already accepted one such request and is a mentor.", requested_by = req.sent_by)
                       req.is_valid = False
                       req.save()

                ## alert all the mentors including who made request and all assigned users
                for a_mentor in task.mentors.all():
                    create_notification(request_obj.role, a_mentor, replied_by, True, task, request_obj.remarks, requested_by)
                for a_user in task.assigned_users.all():
                    create_notification(request_obj.role, a_user, replied_by, True, task, request_obj.remarks, requested_by)

                addMentor(task, request_obj.replied_by)
            else:
                ## tell the requested user that his request was rejected due to these reasons.
                create_notification(request_obj.role, requested_by, replied_by, False, task, request_obj.remarks, requested_by)

        elif request_obj.role == "DV":
            if reply:
                ## tell only the user who made him a DV
                ## drop a welcome message to that fucker
                changeRole(role=request_obj.role, user=request_obj.replied_by)
                create_notification(request_obj.role, request_obj.sent_by, request_obj.replied_by, reply, requested_by=request_obj.sent_by)
            else:
                create_notification(request_obj.role, request_obj.sent_by, request_obj.replied_by, reply, remarks=request_obj.remarks, requested_by=request_obj.sent_by)

        elif request_obj.role == "MG":
            if reply:
                ## tell all the MG and AD
                ## drop a welcome message to that fucker
                changeRole(role=request_obj.role, user=request_obj.replied_by)
                alerting_users = Profile.objects.filter(user__is_active=True).exclude(rights="CT").exclude(rights="DV")
                for a_profile in alerting_users:
                    create_notification(request_obj.role, a_profile.user, request_obj.replied_by, reply, requested_by=request_obj.sent_by)
            else:
                create_notification(request_obj.role, request_obj.sent_by, request_obj.replied_by, reply, remarks=request_obj.remarks, requested_by=request_obj.sent_by)

        elif request_obj.role == "AD":
            if reply:
                ## tell all the AD
                ## drop a welcome message to that fucker
                changeRole(role=request_obj.role, user=request_obj.replied_by)
                alerting_users = Profile.objects.filter(user__is_active=True).filter(rights="AD")
                for a_profile in alerting_users:
                    create_notification(request_obj.role, a_profile.user, request_obj.replied_by, reply, requested_by=request_obj.sent_by)
            else:
                create_notification(request_obj.role, request_obj.sent_by, request_obj.replied_by, reply, remarks=request_obj.remarks, requested_by=request_obj.sent_by)

        return True #Reply has been added successfully
    return False #Already replied

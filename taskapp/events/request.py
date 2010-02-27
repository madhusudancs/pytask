from datetime import datetime
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
                    print "send yes notifications appropriately"
                    #def create_notification(role, sent_to, sent_from=None, reply=None, task=None, remark=None, receiving_user=None, pynts=None, requested_by):
                    create_notification("PY", a_mentor, replied_by, True, task, receiving_user, pynts, requested_by)
                else:
                    print "send a no notificvaton"
                    create_notification("PY", a_mentor, replied_by, False, task, receiving_user, pynts, requested_by, request_obj.remarks)

        elif request_obj.role == "MT":
            ## add him as a mentor to the task
            if reply:
                ## check for the current rights of request_obj.sent_by
                ## what if he is no more a mentor to the task
                addMentor(request_obj.task, request_obj.replied_by)
                ## pass on notification of request_obj.sent_by
            else:
                print "request for mentor rejected"
                ## pass on notification to request_obj.sent_by

        elif request_obj.role in ["AD", "MG", "DV"]:
            if reply:
                ## make him the role
                ## here we check for rights just in case to be fine with demoted users. we change only the user who made request has that rights.
                changeRole(role=request_obj.role, user=request_obj.replied_by)
            else:
                ## notify request_obj.sent_by that it has been rejected
                pass
        return True #Reply has been added successfully
    return False #Already replied

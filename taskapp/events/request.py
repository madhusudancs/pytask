from datetime import datetime
from pytask.taskapp.events.task import addCredits, addMentor

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
            if reply:
                addCredits(request_obj.task, request_obj.sent_by, request_obj.receiving_user, request_obj.pynts)
                print "send yes notifications appropriately"
            else:
                print "send a no notificvaton"
        elif request_obj.role == "MT":
            ## add him as a mentor to the task
            if reply:
                addMentor(request_obj.task, request_obj.replied_by)
                ## pass on notification of request_obj.sent_by
            else:
                print "request for mentor rejected"
                ## pass on notification to request_obj.sent_by

        elif request_obj.role in ["AD", "MG", "DV"]:
            if reply:
                pass
                ## make him the role
                ## changeRole(role=request_obj.role, made_by=request_obj.sent_by)
            else:
                ## notify request_obj.sent_by that it has been rejected
                pass
        return True #Reply has been added successfully
    return False #Already replied

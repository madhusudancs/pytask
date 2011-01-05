from datetime import datetime
from django.contrib.auth.models import User
from pytask.taskapp.models import Notification, RIGHTS_CHOICES

def create_notification(role, sent_to, sent_from=None, reply=None, task=None, remarks=None, requested_by=None, receiving_user=None, pynts=None):
    """
    creates a notification based on the passed arguments.
        role: role of the notification - look at choices in models 
        sent_to: a user to which the notification is to be sent
        sent_from : a user from which the message has originated
            A user who approves/rejects in case of request
            A reviewer who closes/complets the task
        reply: A boolean
        task: a task if applicable
        requested_by: a user makes the request
            A reviewer who assigns pynts in case of pynts
            A reviewer who requests to act as a reviewer
        remarks: any remarks for rejecting
        receiving_user: user receiving pynts
        pynts: the obvious
    """

    notification = Notification(sent_date = datetime.now())
    notification.role = role
    notification.sent_to = sent_to
    notification.save()

    if role == "PY":

        notification.sent_from = sent_from
        notification.task = task
        notification.pynts = pynts

        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)
        pynts_url = '<a href="/task/assignpynts/tid=%s">%s</a>'%(task.id, "click here")
        reviewer_url = '<a href="/user/view/uid=%s">%s</a>'%(requested_by.id, requested_by.username)
        admin_url = '<a href="/user/view/uid=%s">%s</a>'%(sent_from.id, sent_from.username)
        user_url = '<a href="/user/view/uid=%s">%s</a>'%(receiving_user.id, receiving_user.username)

        if reply:
            notification.sub = "Approved request for assign of pynts for %s"%task.title[:20]
            notification.message  = """ Request made by %s to assign %s pynts to %s for the task %s has been approved by %s<br />
                                    %s if you want the view/assign pynts page of the task.<br />"""%(reviewer_url, pynts, user_url, task_url, admin_url, pynts_url)

        else:
            notification.sub = "Rejected request for assign of pynts for %s"%task.title[:20]
            notification.message = """ Request made by %s to assign %s pynts to %s for the task %s has been rejected by %s.<br /> """%(reviewer_url, pynts, user_url, task_url, admin_url)
            if remarks:
                notification.remarks = remarks
                notification.message += "Reason: %s<br />"%remarks
            notification.message += "<br />"

    elif role == "MT":

        notification.task = task
        notification.sent_from = sent_from

        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)
        requested_reviewer_url = '<a href="/user/view/uid=%s">%s</a>'%(requested_by.id, requested_by.username)
        new_reviewer = sent_from
        new_reviewer_url = '<a href="/user/view/uid=%s">%s</a>'%(new_reviewer.id, new_reviewer.username)
        
        if reply:
            notification.sub = "New reviewer for the task %s"%task.title[:20]
            notification.message = "%s has accepted the request made by %s, asking him act as a reviewer for the task %s<br />"%(new_reviewer_url, requested_reviewer_url, task_url)
            notification.message += "He can be contacted on %s"%new_reviewer.email

        else:
            notification.sub = "%s rejected request to act as a reviewer"%new_reviewer.username
            notification.message = "%s has rejected your request asking him to act as a reviewer for %s.<br />"%(new_reviewer_url, task_url)
            if remarks:
                notification.remarks = remarks
                notification.message += "Remarks: %s<br />"%remarks

    elif role in ["DV", "MG", "AD"]:

        notification.sent_from = sent_from
        accepting_user = sent_from
        user_url = '<a href="/user/view/uid=%s">%s</a>'%(accepting_user.id, accepting_user.username) ## i mean the user who has accepted it
        requested_by_url = '<a href="/user/view/uid=%s">%s</a>'%(requested_by.id, requested_by.username)
        role_rights = dict(RIGHTS_CHOICES)[role]
        role_learn_url = "/about/%s"%role_rights.lower()
        a_or_an = "an" if role_rights == "AD" else "a"

        if reply:
            notification.sub = "New %s for the site"%role_rights
            notification.message = "%s has accepted request made by %s asking him to act as %s %s for the website.<br />"%(user_url, requested_by_url, a_or_an, role_rights)
        else:
            notification.sub = "Rejected your request to act as %s"%role_rights
            notification.message = "%s has rejected your request asking him to act as %s %s.<br />"%(user_url, a_or_an, role_rights)
            if remarks:
                notification.remarks = remarks
                notification.message += "Remarks: %s<br />"%remarks

    elif role == "NT":

        notification.task = task
        new_reviewer = sent_to
        reviewer_learn_url = '<sup><a href="/about/reviewer/">learn more</a></sup>'
        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)

        notification.sub = "You are reviewering the task %s"%task.title[:20]
        notification.message = "You have accepted to act as a reviewer%s for the task %s.<br />"%(reviewer_learn_url, task_url)
        notification.message += " Here is a list of other reviewers and their email addresses.<br /> <ul>"

        for a_reviewer in task.reviewers.exclude(id=new_reviewer.id):
            notification.message += "<li> %s - %s </li>"%(a_reviewer.username, a_reviewer.email)
        notification.message += "</ul>"

        working_users = task.assigned_users.all()
        if working_users:
            notification.message += "List of users working on the task.<br />"
            notification.message += "<ul>"
            for a_user in working_users:
                notification.message += "<li> %s - %s </li>"%(a_user.username, a_user.email)
            notification.message += "</ul><br />"
        notification.message += "Happy Reviewering."

    elif role == "NU":

        start_here_url = '<a href="/about/starthere/" taget="_blank">click here</a>'
        notification.sub = "Welcome %s"%sent_to.username
        notification.message = "Welcome to PyTasks %s.<br />"%sent_to.username
        notification.message += "%s to know more."%start_here_url

    elif role in ["ND", "NG", "NA"]:

        rights_dict = dict(RIGHTS_CHOICES)

        if role == "ND":
            role_rights = rights_dict["DV"]
        elif role == "NG":
            role_rights = rights_dict["MG"]
        elif role == "NA":
            role_rights = rights_dict["AD"]

        requested_by_url = r'<a href="/user/view/uid=%s">%s</a>'%(requested_by.id, requested_by.username)
        role_learn_url = r'<a href="/about/%s" target="_blank">click here</a>'%role_rights.lower()
        a_or_an = "an" if role_rights == "Admin" else "a"

        notification.sub = "You are now %s %s"%(a_or_an, role_rights)
        notification.message = r"You have accepted the request made by %s asking you to act as %s %s in the site "%(requested_by_url, a_or_an, role_rights)
        notification.message += "and you are now %s %s in the site.<br /> %s to learn more on %s."%(a_or_an, role_rights, role_learn_url, role_rights)


    elif role in ["CM", "CD"]:

        notification.sent_from = sent_from
        notification.role = role
        notification.task = task
        notification.remarks = remarks

        reviewer = sent_from
        reviewer_url = '<a href="/user/view/uid=%s">%s</a>'%(reviewer.id, reviewer.username)
        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)
        
        if role == "CM":
            notification.sub = "%s has been marked complete"%task.title
            notification.message = "The task %s has been marked complete by %s.<br />"%(task_url, reviewer_url)

        elif role == "CD":
            notification.sub = "%s has been closed"%task.title
            notification.message = "The task %s has been closed by %s.<br />"%(task_url, reviewer_url)

        if remarks:
            notification.remarks = remarks
            notification.message += "<b>Remarks:</b> %s"%remarks

    elif role == "AU":

        notification.task = task
        notification.sent_from = sent_from
        added_user = sent_to
        reviewer = sent_from
        assigned_by_url = '<a href="/user/view/uid=%s">%s</a>'%(reviewer.id, reviewer.username)
        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)

        notification.sub = "Your claim for the task %s accepted."%task.title[:20]
        notification.message = "You have been selected to work on the task %s by %s.<br />"%(task_url, assigned_by_url)
        notification.message += "You can now start working on the task and will be pynted by the reviewers for your work.<br />"

        notification.message += " Here is a list of reviewers for the task and their email addresses.<br /> <ul>"
        for a_reviewer in task.reviewers.all():
            notification.message += "<li> %s - %s </li>"%(a_reviewer.username, a_reviewer.email)
        notification.message += "</ul>"

        working_users = task.assigned_users.exclude(id=added_user.id)
        if working_users:
            notification.message += "List of other users working on the task.<br />"
            notification.message += "<ul>"
            for a_user in working_users:
                notification.message += "<li> %s - %s </li>"%(a_user.username, a_user.email)
            notification.message += "</ul><br />"

    elif role == "RU":

        notification.task = task
        notification.sent_from = sent_from
        removed_user = sent_to
        reviewer = sent_from
        removed_by_url = '<a href="/user/view/uid=%s">%s</a>'%(reviewer.id, reviewer.username)
        task_url = '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)
        claim_url = '<a href="/task/claim/tid=%s">%s</a>'%(task.id, "clicking here")

        notification.sub = "You have been removed from working users of %s"%task.title[:20]
        notification.message = "%s has removed you from the working users list of %s.<br />"%(removed_by_url, task_url)
        notification.message += "if you want to work on the task again, you can claim the task by %s.<br />"%claim_url
        if remarks:
            notification.remarks = remarks
            notification.message += "<b>Reason: </b>%s"%(remarks)

    elif role == "DL":

        notification.sent_from = sent_from
        notification.task = task
        deleted_by_url = '<a href="/user/view/uid=%s">%s</a>'%(sent_from.id, sent_from.username)

        notification.sub = "Task deleted"
        notification.message = 'The unpublished task "%s" viewable by you has been deleted by its creator %s.<br />'%(task.title, deleted_by_url)

        if remarks:
            notification.remarks = remarks
            notification.message += "<b>Reason: </b>%s"%remarks

    elif role == "CL":

        notification.sent_from = sent_from
        notification.task = task
        notification.remarks = remarks

        claimed_by_url = '<a href="/user/view/uid=%s">%s</a>'%(sent_from.id, sent_from.username)
        claim_url = '<a href="/task/claim/tid=%s">claim</a>'%(task.id)
        task_url = '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)

        notification.sub = 'New claim for the task "%s"'%(task.title[:20])
        notification.message = '%s has submitted a %s for the task "%s" reviewered by you.<br />'%(claimed_by_url, claim_url, task_url)
        notification.message += '<b>Claim proposal:</b> %s'%(remarks)



    notification.save()

def mark_notification_read(notification_id):
    """
    makes a notification identified by the notification_id read.
    arguments:
        notification_id - a number denoting the id of the Notification object
    """
    try:
        notification = Notification.objects.get(id = notification_id)
    except Notification.DoesNotExist:
        return False
    notification.is_read = True
    notification.save()
    return True

def delete_notification(notification_id):
    """
    deletes a notification identified by the notification_id.
    arguments:
        notification_id - a number denoting the id of the Notification object
    """
    try:
        notification = Notification.objects.get(id = notification_id)
    except Notification.DoesNotExist:
        return False
    notification.is_deleted = True
    notification.save()
    return True

def get_notification(nid, user):
    """ if notification exists, and belongs to the current user, return it.
    else return None.
    """

    user_notifications = user.notification_sent_to.filter(is_deleted=False).order_by('sent_date')
    current_notifications = user_notifications.filter(id=nid)
    if user_notifications:
        current_notification = current_notifications[0]

        try:
            newer_notification = current_notification.get_next_by_sent_date(sent_to=user, is_deleted=False)
            newest_notification = user_notifications.reverse()[0]
            if newest_notification == newer_notification:
                newest_notification = None
        except Notification.DoesNotExist:
            newest_notification, newer_notification = None, None

        try:
            older_notification = current_notification.get_previous_by_sent_date(sent_to=user, is_deleted=False)
            oldest_notification = user_notifications[0]
            if oldest_notification == older_notification:
                oldest_notification = None
        except:
            oldest_notification, older_notification = None, None

        return newest_notification, newer_notification, current_notification, older_notification, oldest_notification

    else:
        return None, None, None, None, None

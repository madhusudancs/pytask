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
            A mentor who closes/complets the task
        reply: A boolean
        task: a task if applicable
        requested_by: a user makes the request
            A mentor who assigns credits in case of pynts
            A mentor who requests to act as a mentor
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
        credits_url = '<a href="/task/assigncredits/tid=%s">%s</a>'%(task.id, "click here")
        mentor_url = '<a href="/user/view/uid=%s">%s</a>'%(requested_by.id, requested_by.username)
        admin_url = '<a href="/user/view/uid=%s">%s</a>'%(sent_from.id, sent_from.username)
        user_url = '<a href="/user/view/uid=%s">%s</a>'%(receiving_user.id, receiving_user.username)

        if reply:
            notification.sub = "Approved request for assign of credits for %s"%task.title[:20]
            notification.message  = """ Request made by %s to assign %s pynts to %s for the task %s has been approved by %s<br />
                                    %s if you want the view/assign pynts page of the task.<br />"""%(mentor_url, pynts, user_url, task_url, admin_url, credits_url)

        else:
            notification.sub = "Rejected request for assign of credits for %s"%task.title[:20]
            notification.message = """ Request made by %s to assign %s pynts to %s for the task %s has been rejected by %s.<br /> """%(mentor_url, pynts, user_url, task_url, admin_url)
            if remarks:
                notification.remarks = remarks
                notification.message += "Reason: %s<br />"%remarks
            notification.message += "<br />"

    elif role == "MT":

        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)
        requested_mentor_url = '<a href="/user/view/uid=%s">%s</a>'%(requested_by.id, requested_by.username)
        new_mentor = sent_from
        new_mentor_url = '<a href="/user/view/uid=%s">%s</a>'%(new_mentor.id, new_mentor.username)
        
        if reply:
            notification.sub = "New mentor for the task %s"%task.title[:20]
            notification.message = "%s has accepted the request made by %s, asking him act as a mentor for the task %s<br />"%(new_mentor_url, requested_mentor_url, task_url)
            notification.message += "He can be contacted on %s"%new_mentor.email

        else:
            notification.sub = "%s rejected request to act as a mentor"%new_mentor.username
            notification.message = "%s has rejected your request asking him to act as a mentor for %s.<br />"%(new_mentor_url, task_url)
            if remarks:
                notification.message += "Remarks: %s<br />"%remarks

    elif role in ["DV", "MG", "AD"]:

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
                notification.message += "Remarks: %s<br />"%remarks

    elif role == "NT":

        new_mentor = sent_to
        mentor_learn_url = '<sup><a href="/about/mentor">learn more</a></sup>'
        task_url= '<a href="/task/view/tid=%s">%s</a>'%(task.id, task.title)

        notification.sub = "You are mentoring the task %s"%task.title[:20]
        notification.message = "You have accepted to act as a mentor%s for the task %s.<br />"%(mentor_learn_url, task_url)
        notification.message += " Here is a list of other mentors and their email addresses.<br /> <ul>"

        for a_mentor in task.mentors.exclude(id=new_mentor.id):
            notification.message += "<li> %s - %s </li>"%(a_mentor.username, a_mentor.email)
        notification.message += "</ul> List of users working on the task.<br />"

        working_users = task.assigned_users.all()
        if working_users:
            notification_message += "<ul>"
            for a_user in working_users:
                notification.message += "<li> %s - %s </li>"%(a_user.username, a_user.email)
            notification.message += "</ul><br />"
        notification.message += "Happy Mentoring."

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

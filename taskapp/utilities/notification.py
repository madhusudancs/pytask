from datetime import datetime
from django.contrib.auth.models import User
from pytask.taskapp.models import Notification

def create_notification(role, sent_to, sent_from=None, reply=None, task=None, receiving_user=None, pynts=None, requested_by=None, remarks=None):
    """
    creates a notification based on the passed arguments.
        to - a list of users to which the notification is to be sent
        subject - subject of the notification message to be sent
        message - message body of the notification
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
            notification.sub = "Approved request for assign of credits"
            notification.message  = """ Request made by %s to assign %s pynts to %s for the task %s has been approved by %s<br />
                                    %s if you want the view/assign pynts page of the task.<br />"""%(mentor_url, pynts, user_url, task_url, admin_url, credits_url)

        else:
            notification.sub = "Rejected request for assign of credits"
            notification.message = """ Request made by %s to assign %s pynts to %s for the task %s has been rejected by %s.<br /> """%(mentor_url, pynts, user_url, task_url, admin_url)
            if remarks:
                notification.remarks = remarks
                notification.message += "Reason: %s<br />"%remarks
            notification.message += "<br />"

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

    try:
        notify_obj = Notification.objects.get(id=nid)
    except Notification.DoesNotExist:
        return None

    if notify_obj.sent_to == user and ( not notify_obj.is_deleted ):
        return notify_obj

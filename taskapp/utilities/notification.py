from datetime import datetime
from django.contrib.auth.models import User
from pytask.taskapp.models import Notification

def create_notification(to,subject,message):
    """
    creates a notification based on the passed arguments.
        to - a list of users to which the notification is to be sent
        subject - subject of the notification message to be sent
        message - message body of the notification
    """
    notification = Notification(sent_date = datetime.now())
    notification.save()
    notification.sent_to = to
    notification.sub = subject
    notification.message = message
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

    try:
        notify_obj.sent_to.get(id=user.id)
    except User.DoesNotExist:
        return None

    if not notify_obj.is_deleted:
        return notify_obj

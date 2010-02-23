from pytask.taskapp.models import Notification
from datetime import datetime

def create_notification(to,subject,message):
    """
    creates a notification based on the passed arguments.
        to - a list of users to which the notification is to be sent
        subject - subject of the notification message to be sent
        message - message body of the notification
    """
    notification = Notification(sent_date = datetime.now())
    notification.save()
    notification.to = to
    notification.sub = subject
    notification.message = message
    notification.save()

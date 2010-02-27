"""
A collection of utility functions for user.
"""

def get_user(user):
    """ get the no of unread requests and notifications and add them as properties for user.
    """

    unread_notifications = user.notification_sent_to.filter(is_read=False,is_deleted=False).count
    unread_requests = user.request_sent_to.filter(is_valid=True,is_replied=False).count

    user.unread_notifications = unread_notifications
    user.unread_requests = unread_requests

    return user



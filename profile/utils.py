
def get_notification(nid, user):
    """ if notification exists, and belongs to the current user, return it.
    else return None.
    """

    user_notifications = user.notification_sent_to.filter(is_deleted=False).order_by('sent_date')
    current_notifications = user_notifications.filter(uniq_key=nid)
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

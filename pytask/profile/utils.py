#!/usr/bin/env python
#
# Copyright 2011 Authors of PyTask.
#
# This file is part of PyTask.
#
# PyTask is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyTask is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTask.  If not, see <http://www.gnu.org/licenses/>.


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django import shortcuts
from django.http import Http404
from django.contrib.auth.models import User
from pytask.profile.models import Notification

def get_notification(nid, user):
    """ if notification exists, and belongs to the current user, return it.
    else return None.
    """

    user_notifications = user.notification_sent_to.filter(is_deleted=False).order_by('sent_date')
    current_notifications = user_notifications.filter(pk=nid)
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

def get_user(uid):

    user = shortcuts.get_object_or_404(User, pk=uid)

    if user.is_active:
        return user
    else:
        raise Http404

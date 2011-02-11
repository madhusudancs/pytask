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
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    ]


from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url


urlpatterns = patterns('pytask.profile.views',
  url(r'^view/$', 'view_profile', name='view_profile'),
  url(r'^view/(?P<user_id>\d+)$', 'view_profile',
    name='view_user_profile'),
  url(r'^edit/$', 'edit_profile', name='edit_profile'),
  url(r'^notification/browse/$', 'browse_notifications',
      name='browse_notifications'),
  url(r'^notification/view/(?P<notification_id>\d+)$',
      'view_notification', name='view_notification'),
  url(r'^notification/delete/(?P<notification_id>\d+)$',
      'delete_notification', name='delete_notification'),
  url(r'^notification/unread/(?P<notification_id>\d+)$',
      'unread_notification', name='unread_notification'),
  url(r'^user/view/(?P<user_id>\d+)$', 'view_user',
      name='view_user'),
  url(r'^login/proceed$', 'login_proceed', name='login_proceed'),
)

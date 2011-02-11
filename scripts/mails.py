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

# You should have received a copy of the GNU General Public License
# along with PyTask.  If not, see <http://www.gnu.org/licenses/>.


"""Helper script to send emails to the users.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from django.template import loader
from django.contrib.auth.models import User


def textbook_workshop_remainder(subject_template=None, body_template=None,
                                user_filter = None):
    """Sends a mail to each delegate about the template content specified.
    """

    if user_filter:
        users = User.objects.filter(**user_filter)
    else:
        users = User.objects.all()

    subject = loader.render_to_string(subject_template).strip(' \n\t')

    for user in users:
        profile = user.get_profile()
        if profile:
            full_name = profile.full_name
        else:
            full_name = ''

        message = loader.render_to_string(
          body_template, dictionary={'name': full_name})

        user.email_user(subject=subject, message=message,
                        from_email='Madhusudan C.S. <madhusudancs@fossee.in>')


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


from django.db import models

from django.contrib.auth.models import User


GENDER_CHOICES = (
  ('Male', 'Male'),
  ('Female', 'Female'),
)


ROLES_CHOICES = (
  ("Administrator", "Administrator"),
  ("Coordinator", "Coordinator"),
  ("Mentor", "Mentor"),
  ("Contributor", "Contributor"),
)


ROLE_CHOICES = (
  ("Administrator", "Request sent by Administrator \
    to a user at lower level, asking him to act as a administrator"),
  ("Coordinator", "Request sent by Coordinator \
    to a user at lower level, asking him to act as a coordinator"),
)


class Profile(models.Model):
    full_name = models.CharField(
      max_length=50, verbose_name="Name as on bank account",
      help_text="Any DD/Cheque will be issued on this name")

    user = models.ForeignKey(User, unique = True)

    role = models.CharField(max_length=255,
                            choices=ROLES_CHOICES,
                            default=u"Contributor")

    pynts = models.PositiveSmallIntegerField(default=0)

    aboutme = models.TextField(
      blank = True,
      help_text="This information will be used to judge the eligibility "
        "for any task")

    dob = models.DateField(verbose_name=u"Date of Birth",
                           help_text="YYYY-MM-DD")

    gender = models.CharField(verbose_name=u'Gender',
                              max_length=24, choices=GENDER_CHOICES)

    address = models.TextField(
      blank=False, help_text="This information will be used to send "
        "any DDs/Cheques.")

    phonenum = models.CharField(max_length = 15, blank = True,
                                verbose_name = u"Phone Number")

    def __unicode__(self):
        return unicode(self.user.username)


class Notification(models.Model):
    """ A model to hold notifications.
    All these are sent by the site to users.
    Hence there is no sent_from option.
    """

    sent_to = models.ForeignKey(User,
                                related_name = "%(class)s_sent_to",
                                blank = False)

    subject = models.CharField(max_length=100, blank=True)

    message = models.TextField()

    sent_date = models.DateTimeField()

    is_read = models.BooleanField(default = False)

    is_deleted = models.BooleanField(default = False)


class RoleRequest(models.Model):
    """ A request sent by one user to the other.
    Typically requesting to raise one's status.
    """

    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    is_accepted = models.BooleanField(default=False)

    message = models.TextField()

    response = models.TextField()

    sent_from = models.ForeignKey(User,
                                  related_name = "%(class)s_sent_from",
                                  null = True, blank = True)

    sent_date = models.DateTimeField()

    is_read = models.BooleanField(default = False)

    is_deleted = models.BooleanField(default = False)

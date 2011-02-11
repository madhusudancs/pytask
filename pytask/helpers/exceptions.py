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


"""Module containing the exceptions that can be raised.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django.utils.translation import ugettext


DEFAULT_ERROR_MESSAGE = ugettext(
  "There was some error in your request.")

DEFAULT_LOGIN_MESSAGE = ugettext(
  "You have to login to view this page.")


class PyTaskException(Exception):
    """Base exception class to be used through out PyTask
    """

    def __init__(self, message=None, **response_args):
        """Constructor specifying the exception specific attributes.
        """

        if not message:
            message = DEFAULT_ERROR_MESSAGE

        self.message = message
        self.response_args = response_args

        super(PyTaskException, self).__init__()


class UnauthorizedAccess(PyTaskException):
    """Exception that is raised when some one tries to access a view
    without the right priviliges.
    """

    def __init__(self, message=None, **response_args):
        """Constructor specifying the exception specific attributes
        """

        if not message:
            message = DEFAULT_LOGIN_MESSAGE

        response_args['status'] = 401

        super(UnauthorizedAccess, self).__init__(message, **response_args)

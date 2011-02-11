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


"""Module containing the middleware that processes exceptions for PyTask.
"""

__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext

from pytask.helpers.exceptions import PyTaskException
from pytask.helpers.exceptions import UnauthorizedAccess


class ExceptionMiddleware(object):
    """Middleware definition that processes exceptions raised in PyTaskViews.
    """
  
    def process_exception(self, request, exception):
        """Process the exception raised.
        """

        if (isinstance(exception, PyTaskException) or 
          isinstance(exception, UnauthorizedAccess)):
            template = loader.get_template('error.html')
            context = RequestContext(request, {
              'error_message': exception.message
              })
            return HttpResponse(template.render(context))
    
        # let Django handle it
        return None

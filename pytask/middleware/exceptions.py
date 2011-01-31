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

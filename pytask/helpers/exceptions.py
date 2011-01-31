"""Module containing the exceptions that can be raised.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django.utils.translation import ugettext


DEFAULT_LOGIN_MESSAGE = ugettext(
  "You have to login to view this page.")


class UnauthorizedAccess(Exception):
    """Exception that is raised when some one tries to access a view
    without the right priviliges.
    """

    def __init__(self, message=None, **response_args):
        """Constructor specifying the exception specific attributes
        """

        if not message:
            message = DEFAULT_LOGIN_MESSAGE

        self.message = message
        self.response_args = response_args
        self.response_args['status'] = 401

        super(UnauthorizedAccess, self).__init__()

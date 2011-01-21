"""Helper script to send emails to the users.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from django.template import loader
from django.contrib.auth.models import User
from django.utils.translation import ugettext


def textbook_workshop_remainder(subject_template=None, body_template=None):
    """Sends a mail to each delegate about the template content specified.
    """

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
                        from_email='madhusudancs@fossee.in')


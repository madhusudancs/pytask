"""Module containing the context processors for taskapp.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from pytask.helpers import configuration as config_settings


def configuration(request):
    """Context processor that puts all the necessary configuration
    related variables to every RequestContext'ed template.
    """

    return {
      'TASK_CLAIM_ENABLED': config_settings.TASK_CLAIM_ENABLED,
      }

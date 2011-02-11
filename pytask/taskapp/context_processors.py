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

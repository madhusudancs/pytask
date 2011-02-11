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


"""Module containing the templatetags for rendering data especially for
browsing.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django import template


register = template.Library()


@register.inclusion_tag('templatetags/_as_browse_textbooks.html')
def as_list_tasks(tasks, title):
    """Returns a dictionary required to display the list of tasks.
    """

    return {
      'tasks': tasks,
      'title': title.capitalize(),
      }


@register.inclusion_tag('templatetags/_as_modification_display.html')
def as_modification_display(title, user, creation_datatime):
    """Returns a context dictionary containing the fields necessary
    to render the creation/modification.
    """

    return {
      'title': title,
      'user': user,
      'modification_datetime': creation_datatime,
      }


@register.inclusion_tag('templatetags/_as_uberbar.html')
def as_uberbar(message):
    """Returns a context dictionary containing the fields necessary
    to render the uberbar.
    """

    return {
      'message': message,
      }

@register.inclusion_tag('templatetags/_as_tags.html')
def as_tags(tags):
    """Returns a context dictionary containing the fields necessary
    to render list of tags.
    """

    return {
      'tags': tags,
      }

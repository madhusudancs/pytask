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


"""Helper script that contains many utilities.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from tagging.managers import TaggedItem

from pytask.taskapp.models import Task


def remove_textbook_from_chapter():
    """Removes the tag Textbook from Chapter.
    """

    tasks = TaggedItem.objects.get_by_model(Task, 'Chapter')
    for task in tasks:
        tags = task.tags_field.split(',')
        retags = []
        for tag in tags:
            if 'Textbook' not in tag:
                retags.append(tag)
        task.tags_field = ', '.join(retags)
        task.save()

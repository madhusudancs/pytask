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


"""Module containing taskapp views specific utility functions
"""

__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


def get_intial_tags_for_chapter(textbook):
    """Returns the initial tag set for chapter/module for the textbook.

    Args:
        textbook: textbook entity for which the tags should be built.
    """

    tags = textbook.tags_field.split(',')
    rebuild_tags = []
    for tag in tags:
        tag.strip()
        if 'Textbook' not in tag:
            rebuild_tags.append(tag)

    initial_tags = ', '.join(rebuild_tags + ['Chapter'])

    return initial_tags

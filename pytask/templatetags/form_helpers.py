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


"""Module containing the templatetags for constructing forms.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django import template


register = template.Library()


@register.inclusion_tag('templatetags/_as_div_form.html')
def as_div_form(form, form_name, csrf_token, button_label,
                action_url='', file_support=False):
    """Returns a form to be constructed by the template specified.
    """

    return {
      'form': form,
      'form_name': form_name,
      'csrf_token': csrf_token,
      'action_url': action_url,
      'button_label': button_label,
      'file_support': file_support,
    }


@register.inclusion_tag('templatetags/_as_div_field.html')
def as_div_field(field):
    """Returns the field for each div form field.
    """

    return {
      'field': field,
      }

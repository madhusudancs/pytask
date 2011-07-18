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


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    ]


from django.shortcuts import render_to_response
from django.template import RequestContext

from pytask.profile import models as profile_models


def show_msg(user, message, redirect_url=None, url_desc=None):
    """ simply redirect to homepage """

    context = {
      'user': user,
      'message': message,
      'redirect_url': redirect_url,
      'url_desc': url_desc
    }

    return render_to_response('show_msg.html', context)

def home_page(request):
    """ get the user and display info about the project if not logged in.
    if logged in, display info of their tasks.
    """

    user = request.user
    if not user.is_authenticated():
        return render_to_response("index.html", RequestContext(request, {}))

    profile = user.get_profile()

    claimed_tasks = user.claimed_tasks.all()
    selected_tasks = user.selected_tasks.all()
    reviewing_tasks = user.reviewing_tasks.all()
    unpublished_tasks = user.created_tasks.filter(status="UP").all()
    can_create_task = True if profile.role != profile_models.ROLES_CHOICES[3][0] else False

    context = {"profile": profile,
               "claimed_tasks": claimed_tasks,
               "selected_tasks": selected_tasks,
               "reviewing_tasks": reviewing_tasks,
               "unpublished_tasks": unpublished_tasks,
               "can_create_task": can_create_task
              }

    return render_to_response("index.html", RequestContext(request, context))

def under_construction(request):

    return render_to_response("under_construction.html")

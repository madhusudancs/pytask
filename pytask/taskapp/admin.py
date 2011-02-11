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


from django.contrib import admin

from pytask.taskapp.models import Task, TaskComment, TaskClaim,\
                                  WorkReport, ReportComment, PyntRequest,\
                                  TextBook

admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TextBook)
admin.site.register(WorkReport)
admin.site.register(TaskClaim)
admin.site.register(ReportComment)
admin.site.register(PyntRequest)

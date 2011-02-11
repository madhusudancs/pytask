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


from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from registration.views import register

from pytask.profile.forms import CustomRegistrationForm

# This import is not used anywhere else, but is very important to register
# the user registered signal receiver. So please don't remove it. Although
# it against style to put any imports in the end of the file, this is
# intentional so that this import may not be removed accidentally when
# cleaning up other unused imports.
# Although this import is not directly used in this module, but it is
# imported here so that it executes the code which connects the
# user_registered signal sent by the django-registration app. Also, to
# avoid cyclic imports, there is no better place than here.
import pytask.profile.regbackend


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pytask.views.home_page', name='home_page'),
    (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/register/$', register,
        {'form_class': CustomRegistrationForm,
         'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_register'),
    (r'^accounts/', include('registration.urls')),
    (r'^profile/', include('pytask.profile.urls')),
    (r'^task/', include('pytask.taskapp.urls')),
)

# Serve static files in DEVELOPMENT = True mode
if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^pytask/media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^pytask/static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )

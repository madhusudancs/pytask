from django.conf.urls.defaults import *

from registration.views import register
from registration.backends.default import DefaultBackend
import pytask.profile.regbackend

from pytask.profile.forms import CustomRegistrationForm
from pytask.views import home_page

from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pytask/', include('pytask.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './pytask/static/'}),

    url(r'^accounts/register/$', register,
        {'form_class': CustomRegistrationForm,   
         'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_register'),

    (r'^accounts/', include('registration.urls')),
    (r'^profile/', include('pytask.profile.urls')),
    (r'^task/', include('pytask.taskapp.urls')),
    (r'^$', home_page),
)

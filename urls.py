from django.conf.urls.defaults import *

from registration.views import register
from pytask.profile.forms import CustomRegistrationForm

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
            {'document_root': './static/'}),

    url(r'^accounts/register/$', register,
        {'form_class': CustomRegistrationForm},
        name='registration_register'),
    (r'^accounts/', include('registration.urls')),
    (r'^profile/', include('pytask.profile.urls')),
)

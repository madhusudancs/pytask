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

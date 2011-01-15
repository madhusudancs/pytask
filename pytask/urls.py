from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from registration.views import register

from pytask.profile.forms import CustomRegistrationForm


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

from django.conf.urls.defaults import *

from pytask.taskapp.views import create_task

urlpatterns = patterns('',

            (r'^create/$', create_task),
)


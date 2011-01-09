from django.conf.urls.defaults import *

from pytask.taskapp.views import create_task, view_task, claim_task

urlpatterns = patterns('',

            (r'^create/$', create_task),
            (r'^view/tid=(\w+)', view_task),
            (r'^claim/tid=(\w+)', claim_task),
)


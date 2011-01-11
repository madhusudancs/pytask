from django.conf.urls.defaults import *

from pytask.taskapp.views import create_task, view_task, claim_task, \
        select_user, edit_task, create_textbook, view_textbook, \
        browse_tasks, edit_textbook, approve_task, approved_task,\
        browse_textbooks, approve_textbook, approved_textbook

from pytask.views import under_construction

urlpatterns = patterns('',

            (r'^create/$', create_task),
            (r'^edit/tid=(\w+)$', edit_task),
            (r'^view/tid=(\w+)$', view_task),
            (r'^claim/tid=(\w+)$', claim_task),
            (r'^select/tid=(\w+)$', select_user),
            (r'^approve/tid=(\w+)$', approve_task),
            (r'^approved/tid=(\w+)$', approved_task),
            (r'^browse/$', browse_tasks),

            (r'^textbook/create/$', create_textbook),
            (r'^textbook/view/tid=(\w+)/$', view_textbook),
            (r'^textbook/edit/tid=(\w+)/$', edit_textbook),
            (r'^textbook/approve/tid=(\w+)/$', approve_textbook),
            (r'^textbook/approved/tid=(\w+)/$', approved_textbook),
            (r'^textbook/browse/$', browse_textbooks),
)


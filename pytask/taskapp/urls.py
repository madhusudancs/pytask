from django.conf.urls.defaults import *

from pytask.taskapp.views import create_task, view_task, claim_task, \
        select_user, edit_task, create_textbook, view_textbook, \
        browse_textbooks, edit_textbook

from pytask.views import under_construction

urlpatterns = patterns('',

            (r'^create/$', create_task),
            (r'^edit/tid=(\w+)$', edit_task),
            (r'^view/tid=(\w+)$', view_task),
            (r'^claim/tid=(\w+)$', claim_task),
            (r'^select/tid=(\w+)$', select_user),
            (r'^browse/$', under_construction),

            (r'^textbook/create/$', create_textbook),
            (r'^textbook/view/tid=(\w+)/$', view_textbook),
            (r'^textbook/edit/tid=(\w+)/$', edit_textbook),
            (r'^textbook/browse/$', browse_textbooks),
)


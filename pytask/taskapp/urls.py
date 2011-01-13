from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url


urlpatterns = patterns('pytask.taskapp.views',
            url(r'^create/$', 'create_task'),
            url(r'^edit/tid=(\w+)$', 'edit_task'),
            url(r'^view/tid=(\w+)$', 'view_task'),
            url(r'^claim/tid=(\w+)$', 'claim_task'),
            url(r'^select/tid=(\w+)$', 'select_user'),
            url(r'^approve/tid=(\w+)$', 'approve_task'),
            url(r'^approved/tid=(\w+)$', 'approved_task'),
            url(r'^addreviewer/tid=(\w+)$', 'addreviewer'),
            url(r'^view/work/tid=(\w+)$', 'view_work'),
            url(r'^view/report/rid=(\w+)$', 'view_report'),
            url(r'^submit/report/tid=(\w+)$', 'submit_report'),
            url(r'^browse/$', 'browse_tasks'),

            url(r'^textbook/create/$', 'create_textbook'),
            url(r'^textbook/view/tid=(\w+)/$', 'view_textbook'),
            url(r'^textbook/edit/tid=(\w+)/$', 'edit_textbook'),
            url(r'^textbook/approve/tid=(\w+)/$', 'approve_textbook'),
            url(r'^textbook/approved/tid=(\w+)/$', 'approved_textbook'),
            url(r'^textbook/browse/$', 'browse_textbooks'),
)

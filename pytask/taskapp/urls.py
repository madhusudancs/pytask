from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url


urlpatterns = patterns('pytask.taskapp.views.task',
  url(r'^create/$', 'create_task', name='create_task'),
  url(r'^edit/(?P<task_id>\d+)$', 'edit_task', name='edit_task'),
  url(r'^view/(?P<task_id>\d+)$', 'view_task', name='view_task'),
  url(r'^claim/(?P<task_id>\d+)$', 'claim_task', name='claim_task'),
  url(r'^select/(?P<task_id>\d+)$', 'select_user', name='select_user'),
  url(r'^approve/(?P<task_id>\d+)$', 'approve_task',
      name='approve_task'),
  url(r'^approved/(?P<task_id>\d+)$', 'approved_task',
      name='approved_task'),
  url(r'^addreviewer/(?P<task_id>\d+)$', 'addreviewer',
      name='addreviewer_task'),
  url(r'^view/work/(?P<task_id>\d+)$', 'view_work', name='view_work'),
  url(r'^view/report/(?P<report_id>\d+)$', 'view_report',
      name='view_report'),
  url(r'^submit/report/(?P<task_id>\d+)$', 'submit_report',
      name='submit_report'),
  url(r'^browse/$', 'browse_tasks', name='browse_tasks'),
  url(r'^suggest_tags/$', 'suggest_task_tags', name='suggest_task_tags'),
)

# URL patterns specific to textbook projects.
urlpatterns += patterns('pytask.taskapp.views.textbook',
  url(r'^textbook/create/$', 'create_textbook',
      name='create_textbook'),
  url(r'^textbook/view/(?P<task_id>\d+)$', 'view_textbook',
      name='view_textbook'),
  url(r'^textbook/edit/(?P<task_id>\d+)$', 'edit_textbook',
      name='edit_textbook'),
  url(r'^textbook/approve/(?P<task_id>\d+)$', 'approve_textbook',
      name='approve_textbook'),
  url(r'^textbook/approved/(?P<task_id>\d+)$', 'approved_textbook',
      name='approved_textbook'),
  url(r'^textbook/browse/$', 'browse_textbooks',
      name='browse_textbooks'),
  url(r'^textbook/chapter/create/(?P<book_id>\d+)$', 'create_chapter',
      name='create_chapter'),
)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pytask.taskapp.views.user import homepage, register, user_login, user_logout, view_my_profile, edit_my_profile
from pytask.taskapp.views.task import browse_tasks, view_task, create_task, add_mentor, add_tasks, claim_task, assign_task

urlpatterns = patterns('',
    # Example:
    # (r'^pytask/', include('pytask.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    (r'^$', homepage),
    
    (r'^task/browse/$', browse_tasks),
    (r'^task/view/tid=(\d+)$', view_task),
    (r'^task/create/$', create_task),
    (r'^task/addmentor/tid=(\d+)', add_mentor),
    (r'^task/addtasks/tid=(\d+)', add_tasks),
    (r'^task/claim/tid=(\d+)', claim_task),
    (r'^task/assign/tid=(\d+)', assign_task),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/register/$',register),
    (r'^accounts/login/$',user_login),
    (r'^accounts/logout/$',user_logout),
    
    (r'^user/view/uid=(\d+)$', view_my_profile),
    (r'^user/edit/?$', edit_my_profile),

)

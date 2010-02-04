from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pytask.taskapp.views.users import redirect_to_homepage, homepage, register, user_login, user_logout
from pytask.taskapp.views.tasks import browse_tasks, view_task

urlpatterns = patterns('',
    # Example:
    # (r'^pytask/', include('pytask.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    (r'^$', homepage),
    (r'^task/browse/$', browse_tasks),
    (r'^task/view/tid=(\d+)', view_task),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/register/$',register),
    (r'^accounts/login/$',user_login),
    (r'^accounts/logout/$',user_logout)
)

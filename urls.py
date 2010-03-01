from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from pytask.taskapp.views import user as userViews
from pytask.taskapp.views import task as taskViews

from pytask.taskapp.forms.user import RegistrationFormCustom
from registration.views import register

urlpatterns = patterns('',
    # Example:
    # (r'^pytask/', include('pytask.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './images/'}),

    (r'^$', userViews.homepage),
    
    (r'^task/browse/$', taskViews.browse_tasks),
    (r'^task/view/tid=(\w+)$', taskViews.view_task),
    (r'^task/create/$', taskViews.create_task),
    (r'^task/publish/tid=(\w+)/$', taskViews.publish_task),
    (r'^task/addmentor/tid=(\w+)$', taskViews.add_mentor),
    (r'^task/edit/tid=(\w+)$', taskViews.edit_task),
    (r'^task/claim/tid=(\w+)$', taskViews.claim_task),
    (r'^task/assign/tid=(\w+)$', taskViews.assign_task),
    (r'^task/remuser/tid=(\w+)$', taskViews.rem_user),
    (r'^task/addtask/tid=(\w+)$', taskViews.add_tasks),
    (r'^task/remtask/tid=(\w+)$', taskViews.remove_task),
    (r'^task/assigncredits/tid=(\w+)$', taskViews.assign_credits),
    (r'^task/complete/tid=(\w+)$', taskViews.complete_task),
    (r'^task/close/tid=(\w+)$', taskViews.close_task),
    (r'^task/delete/tid=(\w+)$', taskViews.delete_task),
    
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/register/$',register,{'form_class' : RegistrationFormCustom},name='registration_register'),
    (r'^accounts/', include('registration.urls')),
    (r'^accounts/profile/$', userViews.view_my_profile),
    
    (r'^user/view/uid=(\d+)$', userViews.view_my_profile),
    (r'^user/edit/?$', userViews.edit_my_profile),

    (r'^user/requests/$', userViews.browse_requests),
    (r'^user/requests/rid=(\d+)/$', userViews.view_request),
    (r'^user/requests/rid=(\d+)/(\w+)/$', userViews.process_request),

    (r'^user/notifications/$', userViews.browse_notifications),
    (r'^user/notifications/nid=(\d+)/$', userViews.view_notification),
    (r'^user/notifications/nid=(\d+)/(\w+)/$', userViews.edit_notification),
    (r'^user/make/(\w+)/$', userViews.change_rights),

    (r'^about/(\w+)/$', userViews.learn_more),
    
)

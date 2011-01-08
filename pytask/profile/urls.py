from django.conf.urls.defaults import *

from pytask.profile.views import view_profile, edit_profile,\
                                 browse_notifications, view_notification,\
                                 delete_notification, unread_notification

urlpatterns = patterns('',

            (r'^view/$', view_profile),
            (r'^edit/$', edit_profile),
            (r'^notf/browse/$', browse_notifications),
            (r'^notf/view/nid=(\w+)$', view_notification),
            (r'^notf/del/nid=(\w+)$', delete_notification),
            (r'^notf/unr/nid=(\w+)$', unread_notification),
)


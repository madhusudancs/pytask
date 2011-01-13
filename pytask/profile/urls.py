from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url


urlpatterns = patterns('pytask.profile.views',
            url(r'^view/$', 'view_profile'),
            url(r'^edit/$', 'edit_profile'),
            url(r'^notf/browse/$', 'browse_notifications'),
            url(r'^notf/view/nid=(\w+)$', 'view_notification'),
            url(r'^notf/del/nid=(\w+)$', 'delete_notification'),
            url(r'^notf/unr/nid=(\w+)$', 'unread_notification'),
            url(r'^user/view/uid=(\w+)$', 'view_user'),
)

from django.conf.urls.defaults import *

from pytask.profile.views import view_profile, edit_profile,\
                                 browse_notifications

urlpatterns = patterns('',

            (r'^view/$', view_profile),
            (r'^edit/$', edit_profile),
            (r'^notf/browse/$', browse_notifications),
)


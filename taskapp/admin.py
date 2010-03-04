from django.contrib import admin

from pytask.taskapp.models import Profile, Task, Comment, Notification, Request

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Request)

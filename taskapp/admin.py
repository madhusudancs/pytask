from django.contrib import admin

from pytask.taskapp.models import Profile, Task, Credit, Comment, Claim, Notification

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Credit)
admin.site.register(Claim)
admin.site.register(Notification)

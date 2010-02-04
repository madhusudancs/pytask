from django.contrib import admin

from pytask.taskapp.models import Profile, Task, Credit, Comment

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Credit)

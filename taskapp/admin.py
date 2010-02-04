from django.contrib import admin

from pytask.taskapp.models import Profile, Task, Credit, Comment, Claim

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Credit)
admin.site.register(Claim)

from django.contrib import admin

from pytask.taskapp.models.user import Profile
from pytask.taskapp.models.task import Task
from pytask.taskapp.models.credit import Credit
from pytask.taskapp.models.comment import Comment

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Credit)

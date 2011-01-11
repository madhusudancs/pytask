from django.contrib import admin

from pytask.taskapp.models import Task, TaskComment, TaskClaim,\
                                  WorkReport, ReportComment, PyntRequest,\
                                  TextBook

admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TextBook)
admin.site.register(WorkReport)
admin.site.register(TaskClaim)
admin.site.register(ReportComment)
admin.site.register(PyntRequest)

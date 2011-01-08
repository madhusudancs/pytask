from django.db import models
from django.contrib.auth.models import User

import tagging
from tagging.fields import TagField

TASK_STATUS_CHOICES = (
        ("UP", "Unpublished"),
        ("OP", "Open"),
        ("LO", "Locked"),
        ("WR", "Working"),
        ("CD", "Closed"),
        ("DL", "Deleted"),
        ("CM", "Completed"))

TB_STATUS_CHOICES = (
    ("UP", "Unpublished"),
    ("OP", "Open"),
    ("WR", "All tasks have users selected"),
    ("CM", "Completed"))

UPLOADS_DIR = "./pytask/static/uploads"

class Task(models.Model):
    
    uniq_key = models.CharField(max_length = 10, unique = True)
    title = models.CharField(max_length = 100, verbose_name = u"Title", 
                             help_text = u"Keep it simple and below 100 chars.")
    desc = models.TextField(verbose_name = u"Description")

    status = models.CharField(max_length = 2, choices = TASK_STATUS_CHOICES, default = "UP")
    tags_field = TagField(verbose_name = u"Tags", 
                          help_text = u"Give tags seperated by commas") 
    
    pynts = models.PositiveSmallIntegerField(help_text = u"No.of pynts a user \
                                             gets on completing the task")
    created_by = models.ForeignKey(User,
                                   related_name = "%(class)s_created_by")
    approved_by = models.ForeignKey(User, blank = True, null = True,
                                    related_name = "%(class)s_approved_by")
    reviewers = models.ManyToManyField(User, blank = True, null = True,
                                       related_name = "%(class)s_reviewers")

    claimed_users = models.ManyToManyField(User, blank = True, null = True, 
                                           related_name = "%(class)s_claimed_users")
    selected_users = models.ManyToManyField(User, blank = True, null = True, 
                                            related_name = "%(class)s_selected_users")
    
    creation_datetime = models.DateTimeField()
    approval_datetime = models.DateTimeField(blank = True, null = True)
    
    def __unicode__(self):
        return unicode(self.title)

class TaskComment(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey('Task', related_name = "%(class)s_task")
            
    data = models.TextField()
    commented_by = models.ForeignKey(User,
                                     related_name = "%(class)s_created_by")
    deleted_by = models.ForeignKey(User, null = True, blank = True,
                                   related_name = "%(class)s_deleted_by")
    comment_datetime = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.task.title)

class TaskClaim(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey('Task', related_name = "%(class)s_task")
            
    claimed_by = models.ForeignKey(User,
                                   related_name = "%(class)s_created_by")
    proposal = models.TextField()

    comment_datetime = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.task.title)

class WorkReport(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey(Task, related_name = "%(class)s_task")
    submitted_by = models.ForeignKey(User, null = True, blank = True,
                                     related_name = "%(class)s_submitted_by")
    approved_by = models.ForeignKey(User, null = True, blank = True,
                                    related_name = "%(class)s_approved_by")

    data = models.TextField()
    summary = models.CharField(max_length=100, verbose_name="Summary",
                               help_text="A one line summary")
    attachment = models.FileField(upload_to = UPLOADS_DIR)

    revision = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField()

class ReportComment(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    report = models.ForeignKey('WorkReport', related_name = "%(class)s_report")
            
    data = models.TextField()
    commented_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    deleted_by = models.ForeignKey(User, null = True, blank = True,
                                   related_name = "%(class)s_deleted_by")
    comment_datetime = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

class RequestPynts(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey(Task, related_name = "%(class)s_task")
    pynts = models.PositiveIntegerField(default=0, help_text="No.of pynts")

    requested_by = models.ForeignKey(User, 
                                     related_name = "%(class)s_requested_by")
    requested_for = models.ForeignKey(User, 
                                     related_name = "%(class)s_requested_for")

    responded_by = models.ForeignKey(User, null = True, blank = True,
                                    related_name = "%(class)s_responded_by")

    is_accepted = models.BooleanField(default=False)
    remarks = models.CharField(max_length=100, blank=True,
                               help_text="Reason in case of rejection")
            
    request_datetime = models.DateTimeField()
    is_responded = models.BooleanField(default=False)

class TextBook(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    chapters = models.ManyToManyField(Task, related_name="%(class)s_chapters")
    tags_field = TagField(verbose_name="Tags")

    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    approved_by = models.ForeignKey(User, null = True, blank = True,
                                    related_name = "%(class)s_approved_by")

    status = models.CharField(max_length = 2, choices = TB_STATUS_CHOICES, default = "UP")
    creation_datetime = models.DateTimeField()
    approval_datetime = models.DateTimeField(blank = True, null = True)

tagging.register(Task)

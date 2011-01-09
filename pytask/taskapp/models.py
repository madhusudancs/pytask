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
                                   related_name = "created_tasks")
    approved_by = models.ForeignKey(User, blank = True, null = True,
                                    related_name = "approved_tasks")
    reviewers = models.ManyToManyField(User, blank = True, null = True,
                                       related_name = "reviewing_tasks")

    claimed_users = models.ManyToManyField(User, blank = True, null = True, 
                                           related_name = "claimed_tasks")
    selected_users = models.ManyToManyField(User, blank = True, null = True, 
                                            related_name = "selected_tasks")
    
    creation_datetime = models.DateTimeField()
    approval_datetime = models.DateTimeField(blank = True, null = True)
    
    def __unicode__(self):
        return unicode(self.title)

class TaskComment(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey('Task', related_name = "comments")
            
    data = models.TextField(verbose_name="")
    commented_by = models.ForeignKey(User,
                                     related_name = "commented_taskcomments")
    deleted_by = models.ForeignKey(User, null = True, blank = True,
                                   related_name = "deleted_taskcomments")
    comment_datetime = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.task.title)

class TaskClaim(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey('Task', related_name = "claims")
            
    claimed_by = models.ForeignKey(User,
                                   related_name = "claimed_claims")
    proposal = models.TextField()

    claim_datetime = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.task.title)

class WorkReport(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey(Task, related_name = "reports")
    submitted_by = models.ForeignKey(User, null = True, blank = True,
                                     related_name = "submitted_reports")
    approved_by = models.ForeignKey(User, null = True, blank = True,
                                    related_name = "approved_reports")

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
    commented_by = models.ForeignKey(User, 
                                     related_name = "commented_reportcomments")
    deleted_by = models.ForeignKey(User, null = True, blank = True,
                                   related_name = "deleted_reportcomments")
    comment_datetime = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

class PyntRequests(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey(Task, related_name = "pynt_requests")
    pynts = models.PositiveIntegerField(default=0, help_text="No.of pynts")

    requested_by = models.ForeignKey(User, 
                                     related_name = "requested_by_pynts")
    requested_for = models.ForeignKey(User, 
                                     related_name = "requested_for_pynts")

    responded_by = models.ForeignKey(User, null = True, blank = True,
                                    related_name = "responded_requests")

    is_accepted = models.BooleanField(default=False)
    remarks = models.CharField(max_length=100, blank=True,
                               help_text="Reason in case of rejection")
            
    request_datetime = models.DateTimeField()
    is_responded = models.BooleanField(default=False)

class TextBook(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    chapters = models.ManyToManyField(Task, related_name="%(class)s_set")
    tags_field = TagField(verbose_name="Tags")

    created_by = models.ForeignKey(User, related_name = "created_textbooks")
    approved_by = models.ForeignKey(User, null = True, blank = True,
                                    related_name = "approved_textbooks")

    status = models.CharField(max_length = 2, choices = TB_STATUS_CHOICES, default = "UP")
    creation_datetime = models.DateTimeField()
    approval_datetime = models.DateTimeField(blank = True, null = True)

tagging.register(Task)

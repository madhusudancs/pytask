from django.db import models

STATUS_CHOICES = (
        ("UP", "Unpublished"),
        ("OP", "Open"),
        ("LO", "Locked"),
        ("WR", "Working"),
        ("CD", "Closed"),
        ("DL", "Deleted"),
        ("CM", "Completed"))

class Task(models.Model):
    
    uniq_key = models.CharField(max_length = 10, unique = True)
    title = models.CharField(max_length = 100, verbose_name = u"Title", 
                             help_text = u"Keep it simple and below 100 chars.")
    desc = models.TextField(verbose_name = u"Description")

    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = "UP")
    tags_field = TagField(verbose_name = u"Tags", 
                          help_text = u"Give tags seperated by commas") 
    
    pynts = models.PositiveSmallIntegerField(help_text = u"No.of pynts a user \
                                             gets on completing the task")
    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    approved_by = models.ForeignKey(User, related_name = "%(class)s_approved_by")
    reviewers = models.ManyToManyField(User, related_name = "%(class)s_reviewers")

    claimed_users = models.ManyToManyField(User, blank = True, 
                                           related_name = "%(class)s_claimed_users")
    selected_users = models.ManyToManyField(User, blank = True, 
                                            related_name = "%(class)s_selected_users")
    
    creation_datetime = models.DateTimeField()
    
    def __unicode__(self):
        return unicode(self.title)

class TaskComment(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey('Task', related_name = "%(class)s_task")
            
    data = models.TextField()
    commented_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    deleted_by = models.ForeignKey(User, null = True, blank = True,
                                   related_name = "%(class)s_deleted_by")
    comment_datetime = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.task.title)

class TaskClaim(models.Model):

    uniq_key = models.CharField(max_length = 10, unique = True)
    task = models.ForeignKey('Task', related_name = "%(class)s_task")
            
    claimed_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    proposal = models.TextField()

    comment_datetime = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.task.title)


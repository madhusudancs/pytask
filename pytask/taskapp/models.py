from django.db import models

class Task(models.Model):
    
    uniq_key = models.CharField(max_length = 10, unique = True)
    title = models.CharField(max_length = 100, verbose_name = u"Title", help_text = u"Keep it simple and below 100 chars.")
    desc = models.TextField(verbose_name = u"Description")

    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = "UP")
    tags_field = TagField(verbose_name = u"Tags", help_text = u"Give comma seperated tags") 
    
    pynts = models.PositiveSmallIntegerField(help_text = u"No.of pynts a user gets on completing the task")
        
    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")

    claimed_users = models.ManyToManyField(User, blank = True, related_name = "%(class)s_claimed_users")
    assigned_users = models.ManyToManyField(User, blank = True, related_name = "%(class)s_assigned_users")

    reviewers = models.ManyToManyField(User, related_name = "%(class)s_reviewers")
    
    creation_datetime = models.DateTimeField()
    sub_type = models.CharField(max_length=1, choices = (('D','Dependency'),('S','Subtask')), default = 'D')   
    
    def __unicode__(self):
        return unicode(self.title)

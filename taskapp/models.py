import os

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User

import tagging
from tagging.fields import TagField

from pytask.taskapp.utilities.helper import get_key

GENDER_CHOICES = (( 'M', 'Male'), ('F', 'Female'))
RIGHTS_CHOICES = (
	("AD", "Admin"),
	("MG", "Manager"),
	("DV", "Developer"),
	("CT", "Contributor"),)

STATUS_CHOICES = (
    ("UP", "Unpublished"),
    ("OP", "Open"),
    ("LO", "Locked"),
    ("WR", "Working"),
    ("CD", "Closed"),
    ("DL", "Deleted"),
    ("CM", "Completed"))

NOTIFY_CHOICES = (
    ("MT", "Add Mentor"),
    ("DV", "Developer"),
    ("MG", "Manager"),
    ("AD", "Admin"),
    ("PY", "Assign credits"),
    ("CM", "Task completed"),
    ("CD", "Task closed"),
    ("DL", "Task deleted"),
    ("NU", "New User"),
    ("NT", "New Mentor"),
    ("ND", "New Developer"),
    ("NG", "New Manager"),
    ("NA", "New Admin"),
    ("AU", "Assign user"), ## i mean assign the task
    ("RU", "Remove user"), ## remove from working users list in task
)

IMAGES_DIR = "./images"
UPLOADS_DIR = "./uploads"

class CustomImageStorage(FileSystemStorage):

    def path(self, name):
        """ we return images directory path.
        """

        return os.path.join(IMAGES_DIR, name)

    def get_available_name(self, name):
        """ here we are going with username as the name of image.
        """
    
        root, ext = os.path.splitext(name)
        file_name = get_key() + ext
        while self.exists(file_name):
            file_name = get_key() + ext
        return file_name

class Profile(models.Model):
    
    user = models.ForeignKey(User, unique = True)
    dob = models.DateField(verbose_name = u"Date of Birth", help_text = "YYYY-MM-DD")
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    rights = models.CharField(max_length = 2, choices = RIGHTS_CHOICES, default = u"CT")
    credits = models.PositiveSmallIntegerField(default = 0)
    
    aboutme = models.TextField(blank = True)
    foss_comm = TagField()
    phonenum = models.CharField(max_length = 15, blank = True, verbose_name = u"Phone Number")
    homepage = models.URLField(blank = True, verbose_name = u"Homepage/Blog")
    street = models.CharField(max_length = 80, blank = True)
    city = models.CharField(max_length = 25, blank = True)
    country = models.CharField(max_length = 25, blank = True)
    nick = models.CharField(max_length = 20, blank = True)
    photo = models.ImageField(storage = CustomImageStorage(),upload_to = IMAGES_DIR, blank = True)

    def __unicode__(self):
        return unicode(self.user.username)

class Task(models.Model):
    
    prim_key = models.AutoField(primary_key = True)
    id = models.CharField(max_length = 10, unique = True)
    title = models.CharField(max_length = 100, verbose_name = u"Title", help_text = u"Keep it simple and below 100 chars.")
    desc = models.TextField(verbose_name = u"Description")
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = "UP")
    tags_field = TagField() ## must be named some thing decent later on
    
    credits = models.PositiveSmallIntegerField()
    progress = models.PositiveSmallIntegerField(default = 0)
        
    mentors = models.ManyToManyField(User, related_name = "%(class)s_mentors")
    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    claimed_users = models.ManyToManyField(User, blank = True, related_name = "%(class)s_claimed_users")
    assigned_users = models.ManyToManyField(User, blank = True, related_name = "%(class)s_assigned_users")
    
    creation_datetime = models.DateTimeField()
    published_datetime = models.DateTimeField()
    sub_type = models.CharField(max_length=1, choices = (('D','Dependency'),('S','Subtask')), default = 'D')   
    
    def __unicode__(self):
        return unicode(self.title)

class Map(models.Model):

    main = models.ForeignKey('Task', related_name = "%(class)s_main")
    subs = models.ManyToManyField('Task', blank = True, null = True, related_name = "%(class)s_subs")

class Comment(models.Model):
    
    task = models.ForeignKey('Task')
    data = models.TextField()
    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    creation_datetime = models.DateTimeField()
    deleted_by = models.ForeignKey(User, null = True, blank = True, related_name = "%(class)s_deleted_by")
    is_deleted = models.BooleanField()
    attachment = models.FileField(upload_to = UPLOADS_DIR, blank = True)
    
    def __unicode__(self):
        return unicode(self.task.title)

class Claim(models.Model):
    
    task = models.ForeignKey('Task')
    user = models.ForeignKey(User)
    message = models.TextField()
    creation_datetime = models.DateTimeField()

class Request(models.Model):

    sent_to = models.ManyToManyField(User, related_name = "%(class)s_sent_to", blank = False)
    sent_by = models.ForeignKey(User, related_name = "%(class)s_sent_by", blank = False)
    role = models.CharField(max_length = 2, blank = False)
    reply = models.BooleanField(default = False, blank = False)
    remarks = models.TextField(default = "",blank = True)
    
    is_read = models.BooleanField(default = False, blank = False)
    is_valid = models.BooleanField(default = True, blank = False)
    
    creation_date = models.DateTimeField()
    reply_date = models.DateTimeField()
    is_replied = models.BooleanField(default = False)
    replied_by = models.ForeignKey(User, related_name = "%(class)s_replied_by", blank = True, null = True)
    
    task = models.ForeignKey(Task,related_name = "%(class)s_task", blank = True, null = True)
    receiving_user = models.ForeignKey(User, related_name = "%(class)s_receiving_user", blank = True, null = True)
    pynts = models.PositiveIntegerField(default=0)

    def __unicode__(self):

        return u"Request %s %s"%(self.sent_by.username, self.role)

class Notification(models.Model):

    role = models.CharField(max_length = 2, choices = NOTIFY_CHOICES, blank = False)
    sent_to = models.ForeignKey(User, related_name = "%(class)s_sent_to", blank = False)
    sent_from = models.ForeignKey(User, related_name = "%(class)s_sent_from", null = True, blank = True)
    task = models.ForeignKey(Task, related_name = "%(class)s_sent_for", null = True, blank = True)

    sub = models.CharField(max_length = 100)
    message = models.TextField()
    remarks = models.CharField(max_length = 100)

    sent_date = models.DateTimeField()
    is_read = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)

    def __unicode__(self):
        return u"%s %s"%(self.sent_to, self.sent_date.ctime())
    
tagging.register(Profile)
tagging.register(Task)

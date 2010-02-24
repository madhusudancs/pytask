import random
import string
import os
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
import tagging
from tagging.fields import TagField

GENDER_CHOICES = (( 'M', 'Male'), ('F', 'Female'))
RIGHTS_CHOICES = (
	("AD", "Admin"),
	("MN", "Manager"),
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
        name = ''.join([ random.choice(string.uppercase+string.digits) for i in range(10)])+ext
        while self.exists(name):
            name = ''.join([ random.choice(string.uppercase+string.digits) for i in range(10)])+ext
        return name

class Profile(models.Model):
    
    user = models.ForeignKey(User, unique = True)
    dob = models.DateField(verbose_name = u"Date of Birth", help_text = "YYYY-MM-DD")
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    rights = models.CharField(max_length = 2, choices = RIGHTS_CHOICES, default = u"CT")
    credits = models.PositiveSmallIntegerField(default = 0)
    
    aboutme = models.TextField(blank = True)
#    foss_comm = models.CharField(max_length = 80, blank = True, verbose_name = u"Foss Communities", help_text = u"Comma seperated list of foss communities you are involved in.")
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
    
    title = models.CharField(max_length = 100, unique = True, verbose_name = u"Title", help_text = u"Keep it simple and below 100 chars.")
    desc = models.TextField(verbose_name = u"Description")
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = "UP")
#    tags = models.CharField(max_length = 200, blank = True)
    tags_field = TagField()
    
    subs = models.ManyToManyField('self', blank = True, related_name = "%(class)s_parents")
    deps = models.ManyToManyField('self', blank = True, related_name = "%(class)s_deps")
    
    credits = models.PositiveSmallIntegerField()
    progress = models.PositiveSmallIntegerField(default = 0)
        
    mentors = models.ManyToManyField(User, related_name = "%(class)s_mentors")
    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    claimed_users = models.ManyToManyField(User, blank = True, related_name = "%(class)s_claimed_users")
    assigned_users = models.ManyToManyField(User, blank = True, related_name = "%(class)s_assigned_users")
    
    creation_datetime = models.DateTimeField()
    
    #is_claimable = models.BooleanField()
    
    ## not yet decided if attribs after this are to be included
    ## tasktype = "" ## "bugfix"/"enhancement"
    ## priority = "" ## "very urgent"/"urgent"
    
    def __unicode__(self):
        return unicode(self.title)

class Comment(models.Model):
    
    task = models.ForeignKey('Task')
    data = models.TextField()
    created_by = models.ForeignKey(User, related_name = "%(class)s_created_by")
    creation_datetime = models.DateTimeField()
    deleted_by = models.ForeignKey(User, null = True, blank = True, related_name = "%(class)s_deleted_by")
    deleted = models.BooleanField()
    attachment = models.FileField(upload_to = UPLOADS_DIR, blank = True)
    
    def __unicode__(self):
        return unicode(self.task.title)

class Credit(models.Model):
    
    task = models.ForeignKey('Task')
    given_by = models.ForeignKey(User, related_name = "%(class)s_given_by")
    given_to = models.ForeignKey(User, related_name = "%(class)s_given_to")
    points = models.PositiveSmallIntegerField()
    given_time = models.DateTimeField()
    
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
    is_active = models.BooleanField(default = True)
    reply = models.BooleanField(default = False)
    is_read = models.BooleanField(default = False)
    creation_date = models.DateTimeField()
    reply_date = models.DateTimeField()
    is_replied = models.BooleanField(default = False)
    replied_by = models.ForeignKey(User, related_name = "%(class)s_replied_by", blank = False)
    task = models.ForeignKey(Task,related_name = "%(class)s_task", blank = True, null = True)
    receiving_user = models.ForeignKey(User, related_name = "%(class)s_receiving_user", blank = True, null = True)
    pynts = models.PositiveIntegerField(default=0)

    def __unicode__(self):

        return u"Request %s %s"%(self.by.username, self.role)

class Notification(models.Model):

    to = models.ManyToManyField(User, related_name = "%(class)s_to", blank = False)
    is_read = models.BooleanField(default = False)
    sent_date = models.DateTimeField()
    sub = models.CharField(max_length = 100)
    message = models.TextField()
    deleted = models.BooleanField(default = False)
    
tagging.register(Profile)
tagging.register(Task)

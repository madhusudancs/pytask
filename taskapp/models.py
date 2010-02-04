from django.db import models
from django.contrib.auth.models import User

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
	("CL", "Claimed"),
	("AS", "Assigned"),
    ("RO", "Reopened"),
    ("CD", "Closed"),
    ("DL", "Deleted"),
    ("CM", "Completed"))

IMAGES_DIR = "./images"
UPLOADS_DIR = "./uploads"

class Profile(models.Model):
	
    user = models.ForeignKey(User, unique = True)
    dob = models.DateField(help_text = "YYYY-MM-DD")
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    rights = models.CharField(max_length = 2, choices = RIGHTS_CHOICES, default = u"CT")
    credits = models.PositiveSmallIntegerField(default = 0)
    
    aboutme = models.TextField(blank = True)
    foss_comm = models.CharField(max_length = 80, blank = True)
    phonenum = models.CharField(max_length = 15, blank = True)
    homepage = models.URLField(blank = True)
    street = models.CharField(max_length = 80, blank = True)
    city = models.CharField(max_length = 25, blank = True)
    country = models.CharField(max_length = 25, blank = True)
    nick = models.CharField(max_length = 20, blank = True)
#    photo = models.ImageField(upload_to = IMAGES_DIR, blank = True)

    def __unicode__(self):
        return unicode(self.user.username)


class Task(models.Model):
    
    title = models.CharField(max_length = 200, unique = True)
    desc = models.TextField()
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = "UP")
    tags = models.CharField(max_length = 200, blank = True)
    
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
#    deleted_by = models.ForeignKey(User, null = True, blank = True, related_name = "%(class)s_deleted_by")
#    deleted = models.BooleanField()
#    attachment = models.FileField(upload_to = UPLOADS_DIR, blank = True)
    
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
    

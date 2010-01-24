from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (( 'M', 'Male'), ('F', 'Female'))
RIGHTS_CHOICES = (
	("AD", "Admin"),
	("MN", "Manager"),
	("DV", "Developer"),
	("MT", "Mentor"),
	("CT", "Contributor"),
	("GP", "Public"),)

STATUS_CHOICES = (
	("OP", "Open"),
	("CL", "Claimed"),
	("LO", "Locked"),
	("AS", "Assigned"),)

IMAGES_DIR = "./images"
UPLOADS_DIR = "./uploads"

class Person(models.Model):
#class Person(User):
	
    user = models.ForeignKey(User, unique = True)
    aboutme = models.TextField()
    DOB = models.DateField()
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)
    rights = models.CharField(max_length = 2, choices = RIGHTS_CHOICES)
    credits = models.PositiveSmallIntegerField()
    
    foss_comm = models.CharField(max_length = 80, blank = True)
    phoneNum = models.CharField(max_length = 15, blank = True)
    homepage = models.URLField(blank = True)
    street = models.CharField(max_length = 80, blank = True)
    city = models.CharField(max_length = 25, blank = True)
    country = models.CharField(max_length = 25, blank = True)
    nick = models.CharField(max_length = 20, blank = True)
    photo = models.ImageField(upload_to = IMAGES_DIR, blank = True)

    def __unicode__(self):
        return unicode(self.user.username)


class Task(models.Model):
    
    title = models.CharField(max_length = 200, unique = True)
    desc = models.TextField()
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES)
    tags = models.CharField(max_length = 200, blank = True)
    
    parents = models.ManyToManyField('self', blank = True, related_name = "%(class)s_parents")
    deps = models.ManyToManyField('self', blank = True, related_name = "%(class)s_deps")
    
    credits = models.PositiveSmallIntegerField()
    progress = models.PositiveSmallIntegerField()
        
    mentors = models.ManyToManyField('Person', related_name = "%(class)s_mentors")
    created_by = models.ForeignKey('Person', related_name = "%(class)s_created_by")
    claimed_users = models.ManyToManyField('Person', blank = True, related_name = "%(class)s_claimed_users")
    assigned_users = models.ManyToManyField('Person', blank = True, related_name = "%(class)s_assigned_users")
    
    creation_date = models.DateField()
    
    ## not yet decided if attribs after this are to be included
    ## tasktype = "" ## "bugfix"/"enhancement"
    ## priority = "" ## "very urgent"/"urgent"
    
    def __unicode__(self):
        return unicode(self.title)

class Comment(models.Model):
    
    task = models.ForeignKey('Task')
    data = models.TextField()
    created_by = models.ForeignKey('Person', related_name = "%(class)s_created_by")
    deleted_by = models.ForeignKey('Person', null = True, blank = True, related_name = "%(class)s_deleted_by")
    creation_date = models.DateField()
    deleted = models.BooleanField()
    attachment = models.FileField(upload_to = UPLOADS_DIR, blank = True)
    
    def __unicode__(self):
        return unicode(self.task.title)

class Credit(models.Model):
    
    task = models.ForeignKey('Task')
    given_by = models.ForeignKey('Person', related_name = "%(class)s_given_by")
    given_to = models.ForeignKey('Person', related_name = "%(class)s_given_to")
    points = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return unicode(self.task.title)
    

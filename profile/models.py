from django.db import models

from django.contrib.auth.models import User

GENDER_CHOICES = (( 'M', 'Male'), ('F', 'Female'))

RIGHTS_CHOICES = (
	("DC", "Director"),
	("MG", "Manager"),
	("CT", "Contributor"),)

class Profile(models.Model):
    
    user = models.ForeignKey(User, unique = True)
    rights = models.CharField(max_length = 2, choices = RIGHTS_CHOICES, default = u"CT")
    pynts = models.PositiveSmallIntegerField(default = 0)
    
    aboutme = models.TextField(blank = True, help_text="This information will\
                               be used to judge the eligibility for any task")

    dob = models.DateField(verbose_name = u"Date of Birth", help_text = "YYYY-MM-DD")
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)

    address = models.TextField(blank = False, help_text="This information will\
                               be used to send any DDs/Cheques")
    phonenum = models.CharField(max_length = 15, blank = True, verbose_name = u"Phone Number")

    def __unicode__(self):
        return unicode(self.user.username)

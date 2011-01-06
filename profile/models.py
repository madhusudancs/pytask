from django.db import models

from django.contrib.auth.models import User

GENDER_CHOICES = (( 'M', 'Male'), ('F', 'Female'))

RIGHTS_CHOICES = (
	("DC", "Director"),
	("MG", "Manager"),
        ("CR", "Co-ordinator"),
	("CT", "Contributor"),)

ROLE_CHOICES = (
	("DC", "Request sent by Director \
                to a user at lower level, asking him to act as a director"),
	("MG", "Request sent by Manager \
                to a user at lower level, asking him to act as a manager"),)

class Profile(models.Model):
    
    uniq_key = models.CharField(max_length=20)

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

class Notification(models.Model):
    """ A model to hold notifications.
    All these are sent by the site to users.
    Hence there is no sent_from option.
    """

    uniq_key = models.CharField(max_length=20)

    sent_to = models.ForeignKey(User, related_name = "%(class)s_sent_to", blank = False)
    sent_from = models.ForeignKey(User, related_name = "%(class)s_sent_from", null = True, blank = True)

    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    sent_date = models.DateTimeField()
    is_read = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)

class RoleRequest(models.Model):
    """ A request sent by one user to the other.
    Typically requesting to raise one's status.
    """

    uniq_key = models.CharField(max_length=20)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    is_accepted = models.BooleanField(default=False)

    message = models.TextField()
    response = models.TextField()

    sent_to = models.ForeignKey(User, related_name = "%(class)s_sent_to", blank = False)
    sent_from = models.ForeignKey(User, related_name = "%(class)s_sent_from", null = True, blank = True)

    sent_date = models.DateTimeField()
    is_read = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)


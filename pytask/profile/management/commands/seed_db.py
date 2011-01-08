import sys
from datetime import datetime
from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

from pytask.profile.models import Profile, Notification
from pytask.utils import make_key

def seed_db():
    """ a method to seed the database with random data """
    
    
    for i in range(21,1,-1):
        
        username = 'user'+str(i)
        email = username+'@example.com'
        password = '123456'
        full_name = "User "+str(i)
        dob = datetime.now()
        gender = "M"
        aboutme = "I am User"+str(i)
        address = "I live in street"+str(i)
        phonenum = "1234567890"

        new_user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)

        new_profile = Profile()
        new_profile.user = new_user
        new_profile.full_name = full_name
        new_profile.dob = dob
        new_profile.aboutme = aboutme
        new_profile.gender = gender
        new_profile.address = address
        new_profile.phonenum = phonenum
        if i%2 == 0:
            new_profile.rights = "CT"
        elif i%3 == 0:
            new_profile.rights = "CR"
        new_profile.save()

    new_user.is_superuser = True
    new_user.is_staff = True
    new_user.save()

    for i in range(10):
        Notification(sent_to=new_user, sent_date=datetime.now(), 
                     subject="A subject here for"+str(i),
                     message="A message with mess"+str(i)+" html inside.\
                     <br /><b>a bold text</b>",
                     uniq_key=make_key(Notification),
                    ).save()

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """ Just copied the code from seed_db.py """
        
        seed_db()

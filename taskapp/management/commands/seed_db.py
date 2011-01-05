import sys
from datetime import datetime
from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

from pytask.taskapp.events import task as taskEvents
from pytask.taskapp.events import user as userEvents

from pytask.taskapp.utilities.request import create_request
from pytask.taskapp.utilities.notification import create_notification


def seed_db():
    """ a method to seed the database with random data """
    
    defaultReviewer = userEvents.createSuUser("admin", "admin@example.com", "123456", datetime.now(), "M")
    reviewer_profile = defaultReviewer.get_profile()
    userEvents.updateProfile(reviewer_profile, {'rights':"AD"})
    
    for i in range(1,21):
        
        username = 'user'+str(i)
        email = username+'@example.com'
        password = '123456'
        dob = datetime.now()
        gender = "M"
        user = userEvents.createUser(username,email,password,dob,gender)
        create_notification("NU", user)

        if i%4==0:
            create_request(defaultReviewer, "MG", user)
        elif i%3==0:
            create_request(defaultReviewer, "DV", user)
        elif i%2==0:
            create_request(defaultReviewer, "AD", user)
        elif i in [7, 13]:
            user.is_active = False
            user.save()

    for i in range(1,21):
        
        title = "Task "+str(i)
        desc = "I am "+title
        created_by = defaultReviewer
        pynts = 20
        
        task = taskEvents.createTask(title,desc,created_by,pynts)
        if task:
            taskEvents.addReviewer(task, defaultReviewer)
            if i%2==0:taskEvents.publishTask(task)

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """ Just copied the code from seed_db.py """
        
        seed_db()

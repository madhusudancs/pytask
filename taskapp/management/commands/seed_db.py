import sys
from datetime import datetime
from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

from pytask.taskapp.events import task as taskEvents
from pytask.taskapp.events import user as userEvents

from pytask.taskapp.utilities.request import create_request


def seed_db():
    """ a method to seed the database with random data """
    
    defaultMentor = userEvents.createSuUser("admin", "admin@example.com", "123456", datetime.now(), "M")
    mentor_profile = defaultMentor.get_profile()
    userEvents.updateProfile(mentor_profile, {'rights':"AD"})
    
    for i in range(1,21):
        
        username = 'user'+str(i)
        email = username+'@example.com'
        password = '123456'
        dob = datetime.now()
        gender = "M"
        user = userEvents.createUser(username,email,password,dob,gender)

        if i%4==0:
            create_request(defaultMentor, "MG", user)
        elif i%3==0:
            create_request(defaultMentor, "DV", user)
        elif i%2==0:
            create_request(defaultMentor, "AD", user)
        elif i in [7, 13]:
            user.is_active = False
            user.save()

    for i in range(1,21):
        
        title = "Task "+str(i)
        desc = "I am "+title
        created_by = defaultMentor
        credits = 20
        
        task = taskEvents.createTask(title,desc,created_by,credits)
        if task:
            taskEvents.addMentor(task, defaultMentor)
            if i%2==0:taskEvents.publishTask(task)

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        """ Just copied the code from seed_db.py """
        
        seed_db()

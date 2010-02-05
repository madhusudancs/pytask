from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from pytask.taskapp.events import task as taskEvents
from pytask.taskapp.events import user as userEvents

def seed_db(request):
    """ a method to seed the database with random data """
    
    defaultMentor = userEvents.createSuUser("admin", "admin@example.com", "123456", datetime.now(), "M")
    
    for i in range(1,10):
        
        username = 'user'+str(i)
        email = username+'@example.com'
        password = '123456'
        dob = datetime.now()
        gender = "M"
        userEvents.createUser(username,email,password,dob,gender)

    for i in range(1,21):
        
        title = "Task "+str(i)
        desc = "I am "+title
        created_by = defaultMentor
        credits = 20
        
        task = taskEvents.createTask(title,desc,created_by,credits)
        if task:
            taskEvents.addMentor(task, defaultMentor)
            taskEvents.publishTask(task)
        
    return HttpResponse("Done")

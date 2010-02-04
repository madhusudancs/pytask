from django.contrib.auth.models import User
from pytask.taskapp.models import Profile, Task, Comment, Credit

""" A collection of helper methods. note that there is no validation done here.
we take care of validation and others checks in methods that invoke these methods.
"""

def updateProfile(user_profile, properties):
    """ updates the given properties in the profile for a user. 
    args:
        user_profile : a profile object
        properties : a dictionary with attributes to set as keys and corresponding values
    """
    
    for attr,value in properties.items():
        user_profile.__setattr__(attr,value)
    user_profile.save()

def createUser(username,email,password,dob,gender):
    """ create a user and create a profile and update its properties 
    args:
        username : a username that does not exist
        email : a valid email
        password : a password
        dob : a date object
        gender : u'M'/u'F' 
    """

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    properties = {'dob':dob, 'gender':gender}
    user_profile = Profile(user=user)
    updateProfile(user_profile, properties)
    return user
    
def createSuUser(username,email,password,**properties):
    """ create user using createUser method and set the is_superuser flag """
    
    su_user = createUser(username,email,password,**properties)
    su_user.is_staff = True
    su_user.is_superuser = True
    su_user.save()

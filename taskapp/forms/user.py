#!/usr/bin/python2.5

from django import forms
from pytask.taskapp.models import GENDER_CHOICES, Profile
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

class UserProfileEditForm(forms.ModelForm):
    """Form used to edit the profile of a user"""
    
    class Meta:
        model = Profile
        exclude = ('user','rights','dob','credits')

class RegistrationFormCustom(RegistrationFormUniqueEmail):
    """Used instead of RegistrationForm used by default django-registration backend, this adds date of birth and gender to the default django-registration RegistrationForm"""
    
    dob = forms.DateField(help_text = "YYYY-MM-DD", required=True, label=u'date of birth')
    gender = forms.ChoiceField(choices = GENDER_CHOICES, required=True, label=u'gender')
    
    def save(self,profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],password=self.cleaned_data['password1'],email=self.cleaned_data['email'])
        
        new_profile = Profile(user=new_user,dob=self.cleaned_data['dob'],gender=self.cleaned_data['gender'])
        new_profile.save()
        
        return new_user

def UserChoiceForm(choices, instance=None):
    """ take a list of users and return a choice form.
    """

    class myForm(forms.Form):
        user = forms.ChoiceField(choices, required=True)
    return myForm(instance) if instance else myForm()

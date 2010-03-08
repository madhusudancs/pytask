#!/usr/bin/python2.5

import os
import PIL

from pytask.taskapp.utilities.helper import get_key

from django import forms
from pytask.taskapp.models import GENDER_CHOICES, Profile
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from pytask.taskapp.utilities.notification import create_notification

class UserProfileEditForm(forms.ModelForm):
    """Form used to edit the profile of a user"""
    
    class Meta:
        model = Profile
        exclude = ('user','rights','dob','credits')

    def clean_photo(self):
        uploaded_photo = self.data.get('photo', None)
        prev_photo = self.instance.photo
        if uploaded_photo:
            if uploaded_photo.size > 1048576:
                raise forms.ValidationError('Images only smaller than 1MB allowed')
            tmp_im_path = '/tmp/'+get_key()
            tmp_file = open(tmp_im_path, 'w')
            tmp_file.write(uploaded_photo.read())
            tmp_file.close()
            try:
                PIL.Image.open(tmp_im_path)
            except IOError:
                raise forms.ValidationError('Image format unknown')
            os.remove(tmp_im_path)

            if prev_photo: os.remove(prev_photo.path)
            return uploaded_photo
        else:
            return prev_photo


class RegistrationFormCustom(RegistrationFormUniqueEmail):
    """Used instead of RegistrationForm used by default django-registration backend, this adds date of birth and gender to the default django-registration RegistrationForm"""
    
    dob = forms.DateField(help_text = "YYYY-MM-DD", required=True, label=u'date of birth')
    gender = forms.ChoiceField(choices = GENDER_CHOICES, required=True, label=u'gender')
    
    def save(self,profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],password=self.cleaned_data['password1'],email=self.cleaned_data['email'])
        
        new_profile = Profile(user=new_user,dob=self.cleaned_data['dob'],gender=self.cleaned_data['gender'])
        new_profile.save()
        
        create_notification('NU',new_user)
        
        return new_user

def UserChoiceForm(choices, instance=None):
    """ take a list of users and return a choice form.
    """

    class myForm(forms.Form):
        user = forms.ChoiceField(choices, required=True)
    return myForm(instance) if instance else myForm()

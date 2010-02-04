#!/usr/bin/python2.5

from django import forms
from pytask.taskapp.models import GENDER_CHOICES, Profile
from django.forms import ModelForm

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=60, required=True, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=60, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(max_length=30, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required = True)
    dob = forms.DateField(required=True, help_text = "(YYYY-MM-DD)")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=60, required=True, widget=forms.PasswordInput)

class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','rights')
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['dob'].widget.attrs['readonly'] = True
            self.fields['gender'].widget.attrs['readonly'] = True
            self.fields['credits'].widget.attrs['readonly'] = True
            self.fields['aboutme'].widget.attrs['readonly'] = True
            self.fields['foss_comm'].widget.attrs['readonly'] = True
            self.fields['phonenum'].widget.attrs['readonly'] = True
            self.fields['homepage'].widget.attrs['readonly'] = True
            self.fields['street'].widget.attrs['readonly'] = True
            self.fields['city'].widget.attrs['readonly'] = True
            self.fields['country'].widget.attrs['readonly'] = True
            self.fields['nick'].widget.attrs['readonly'] = True
        #fields = ['dob','gender','credits','aboutme','foss_comm','phonenum','homepage','street','city','country','nick']

class UserProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','rights','dob','credits')

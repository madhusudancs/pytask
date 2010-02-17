#!/usr/bin/python2.5

from django import forms
from pytask.taskapp.models import GENDER_CHOICES, Profile
from django.forms import ModelForm

class UserProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','rights','dob','credits')

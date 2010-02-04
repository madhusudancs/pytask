#!/usr/bin/python2.5

from django import forms
from pytask.taskapp.models import GENDER_CHOICES

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

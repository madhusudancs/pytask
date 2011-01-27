import os
import re

from django import forms
from django.utils.translation import ugettext

from registration.forms import RegistrationFormUniqueEmail
from registration.forms import attrs_dict
from registration.models import RegistrationProfile

from pytask.profile.models import GENDER_CHOICES, Profile

class CustomRegistrationForm(RegistrationFormUniqueEmail):
    """Used instead of RegistrationForm used by default django-registration
    backend, this adds aboutme, dob, gender, address, phonenum to the default 
    django-registration RegistrationForm"""

    # overriding only this field from the parent Form Class since we 
    # don't like the restriction imposed by the registration app on username
    # GMail has more or less set the standard for user names
    username = forms.CharField(
      max_length=30, widget=forms.TextInput(attrs=attrs_dict),
      label=ugettext('Username'), help_text='Username can contain alphabet, '
      'numbers or special characters underscore (_) and (.)')

    full_name = forms.CharField(required=True, max_length=50, 
                                label="Name as on your bank account", 
                                help_text="Any DD/Cheque will be issued on \
                                           this name")

    aboutme = forms.CharField(required=True, widget=forms.Textarea, 
                              max_length=1000, label=u"About Me",
                              help_text="A write up about yourself to aid the\
                              reviewer in judging your eligibility for a task.\
                              It can have your educational background, CGPA,\
                              field of interests etc.,"
                             )


    dob = forms.DateField(help_text = "yyyy-mm-dd", required=True,
                          label=u'Date of Birth')

    gender = forms.ChoiceField(choices = GENDER_CHOICES,
                               required=True, label=u'Gender')

    address = forms.CharField(
      required=True, max_length=200, widget=forms.Textarea,
      help_text="This information will be used while sending DD/Cheque")

    phonenum = forms.CharField(required=True, max_length=10, 
                               label="Phone Number")

    def clean_username(self):
        """Add additional cleaner for username than the parent class
        supplied cleaner.
        """

        username = self.cleaned_data['username']

        # None of the regular expression works better than this custom
        # username check.
        if not re.match(r'^\w+', username):
            raise forms.ValidationError(
              ugettext('Username can start only with an alphabet or a number'))
        elif not re.search(r'\w+$', username):
            raise forms.ValidationError(
              ugettext('Username can end only with an alphabet or a number'))
        elif re.search(r'\.\.+', username):
            raise forms.ValidationError(
              ugettext('Username cannot not have consecutive periods(.)'))

        return super(CustomRegistrationForm, self).clean_username()

    def clean_aboutme(self):
        """ Empty not allowed """

        data = self.cleaned_data['aboutme']
        if not data.strip():
            raise forms.ValidationError("Please write something about\
                                        yourself")

        return data

    def clean_address(self):
        """ Empty not allowed """

        data = self.cleaned_data['address']
        if not data.strip():
            raise forms.ValidationError("Please enter an address")
        
        return data

    def clean_phonenum(self):
        """ should be of 10 digits """

        data = self.cleaned_data['phonenum']

        if (not data.strip()) or \
           (data.strip("1234567890")) or \
           (len(data)!= 10):
               raise forms.ValidationError("This is not a valid phone number")

        return data

    
    def save(self, profile_callback=None):

        new_user = RegistrationProfile.objects.create_inactive_user(
                       username=self.cleaned_data['username'],
                       password=self.cleaned_data['password1'],
                       email=self.cleaned_data['email'])
        
        new_profile = Profile(user=new_user,
                              aboutme=self.cleaned_data['aboutme'],
                              dob=self.cleaned_data['dob'],
                              gender=self.cleaned_data['gender'],
                              address=self.cleaned_data['address'],
                              phonenum=self.cleaned_data['phonenum'],
                             )
        new_profile.save()

        return new_user


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['pynts', 'role']

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['full_name', 'aboutme', 'gender', 'dob', 'address', 'phonenum']

    def clean_aboutme(self):
        """ Empty not allowed """

        data = self.cleaned_data['aboutme']
        if not data.strip():
            raise forms.ValidationError("Please write something about\
                                        yourself")

        return data

    def clean_address(self):
        """ Empty not allowed """

        data = self.cleaned_data['address']
        if not data.strip():
            raise forms.ValidationError("Please enter an address")
        
        return data

    def clean_phonenum(self):
        """ should be of 10 digits """

        data = self.cleaned_data['phonenum']

        if (not data.strip()) or \
           (data.strip("1234567890")) or \
           (len(data)!= 10):
               raise forms.ValidationError("This is not a valid phone number")

        return data

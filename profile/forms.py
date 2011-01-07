import os
import PIL

from django import forms

from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

from pytask.utils import make_key
from pytask.profile.models import GENDER_CHOICES, Profile

class CustomRegistrationForm(RegistrationFormUniqueEmail):
    """Used instead of RegistrationForm used by default django-registration
    backend, this adds aboutme, dob, gender, address, phonenum to the default 
    django-registration RegistrationForm"""

    aboutme = forms.CharField(required=True, max_length=1000, label=u"About Me",
                              help_text="A write up about yourself to aid the\
                              reviewer in judging your eligibility for a task.\
                              It can have your educational background, CGPA,\
                              field of interests etc.,"
                             )

    
    dob = forms.DateField(help_text = "YYYY-MM-DD", required=True, label=u'date of birth')
    gender = forms.ChoiceField(choices = GENDER_CHOICES, required=True, label=u'gender')

    address = forms.CharField(required=True, max_length=200, help_text="This \
                             information will be used while sending DD/Cheque")
    phonenum = forms.CharField(required=True, max_length=10, 
                               label="Phone Number")

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

    
    def save(self,profile_callback=None):

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
                              uniq_key=make_key(Profile),
                             )
        new_profile.save()
        
        return new_user

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['aboutme', 'gender', 'dob', 'address', 'phonenum']

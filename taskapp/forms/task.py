from django import forms
from pytask.taskapp.models import Task, Claim

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desc', 'tags_field', 'credits']
    publish = forms.BooleanField(required=False)

def AddMentorForm(choices,instance=None):
    """ return a form object with appropriate choices """
    
    class myform(forms.Form):
        mentor = forms.ChoiceField(choices=choices, required=True)
    form = myform(instance=instance) if instance else myform()
    return form

class ClaimTaskForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['message']

def AssignTaskForm(choices, instance=None):
    """ return a form object with appropriate choices """
    
    class myform(forms.Form):
        user = forms.ChoiceField(choices=choices, required=True)
    form = myform()
    return form

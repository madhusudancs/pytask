from django import forms
from pytask.taskapp.models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desc', 'tags', 'credits']
    publish = forms.BooleanField(required=False)

def AddMentorForm(choices,instance=None):
    """ return a form object with appropriate choices """
    
    class myform(forms.Form):
        mentor = forms.ChoiceField(choices=choices, required=True)
    form = myform(instance=instance) if instance else myform()
    return form

def ClaimTaskForm(models.ModelForm):
    class Meta:
        model = Claim
        fields = ['message']

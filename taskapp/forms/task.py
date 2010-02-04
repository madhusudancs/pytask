from django import forms
from pytask.taskapp.models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desc', 'tags', 'credits']
    publish = forms.BooleanField(required=False)

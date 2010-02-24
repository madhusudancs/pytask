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

def AddTaskForm(task_choices, is_plain=False):
    """ if is_plain is true, it means the task has no subs/deps.
    so we also give a radio button to choose between subs and dependencies.
    else we only give choices.
    """

    class myForm(forms.Form):
        if is_plain:
            type_choices = [('S','Subtasks'),('D','Dependencies')]
            type = forms.ChoiceField(type_choices, widget=forms.RadioSelect)

        task = forms.MultipleChoiceField(choices=task_choices)
    return myForm()

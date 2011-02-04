from django import forms
from pytask.taskapp.models import Task, WorkReport, TaskComment, TaskClaim, \
                                  TextBook

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desc', 'tags_field', 'pynts']

    def clean_title(self):

        data = self.cleaned_data['title'].strip()

        if not data:
            raise forms.ValidationError("This field is required")

        try:
            Task.objects.exclude(status="DL").get(title__iexact=data)
            raise forms.ValidationError("Another task with same title exists")
        except Task.DoesNotExist:
            return data

    def clean_desc(self):

        data = self.cleaned_data['desc'].strip()

        if not data:
            raise forms.ValidationError("This field is required")

        return data

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'desc', 'tags_field', 'pynts']

    def clean_desc(self):
        data = self.cleaned_data['desc'].strip()
        if not data:
            raise forms.ValidationError("Enter some description for the task")

        return data

    def clean_title(self):
        data = self.cleaned_data['title'].strip()
        try:
            prev_task = Task.objects.exclude(status="DL").get(title__iexact=data)
            if prev_task.id != self.instance.id:
                raise forms.ValidationError("Another task with same title exists")
            else:
                return data
        except Task.DoesNotExist:
            return data

class TaskCommentForm(forms.ModelForm):

    class Meta:
        model = TaskComment
        fields = ['data']

    def clean_data(self):

        data = self.cleaned_data['data'].strip()
        if not data:
            raise forms.ValidationError("Please add some content")

        return data

class ClaimTaskForm(forms.ModelForm):

    class Meta:
        model = TaskClaim
        fields = ["proposal"]

    def clean_proposal(self):
        data = self.cleaned_data['proposal'].strip()
        if not data:
            raise forms.ValidationError('Enter something as a proposal')
        return data

def ChoiceForm(choices, data=None, label="choice"):
    """ return a form object with appropriate choices """
    
    class myform(forms.Form):
        choice = forms.ChoiceField(choices=choices, required=True, label=label)
    form = myform(data) if data else myform()
    return form

class CreateTextbookForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'chapters', 'tags_field']

class CreateChapterForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'desc' , 'pynts', 'tags_field']

class EditTextbookForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'desc', 'pynts', 'tags_field']

def AddTaskForm(task_choices, is_plain=False):
    """ if is_plain is true, it means the task has no subs/deps.
    so we also give a radio button to choose between subs and dependencies.
    else we only give choices.
    """

    class myForm(forms.Form):
        if is_plain:
            type_choices = [('S','Subtasks'),('D','Dependencies')]
            type = forms.ChoiceField(type_choices, widget=forms.RadioSelect)

        task = forms.ChoiceField(choices=task_choices)
    return myForm()

def AssignPyntForm(choices, instance=None):
    
    class myForm(forms.Form):
        user = forms.ChoiceField(choices=choices, required=True)
        pynts = forms.IntegerField(min_value=0, required=True, help_text="Choose wisely since it cannot be undone.")
    return myForm(instance) if instance else myForm()

def RemoveUserForm(choices, instance=None):

    class myForm(forms.Form):
        user = forms.ChoiceField(choices=choices, required=True)
        reason = forms.CharField(min_length=1, required=True)
    return myForm(instance) if instance else myForm()

class WorkReportForm(forms.ModelForm):

    class Meta:
        model = WorkReport
        fields = ['data', 'summary', 'attachment']


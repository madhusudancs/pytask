from django import forms
from pytask.taskapp.models import Task, WorkReport

class TaskCreateForm(forms.ModelForm):
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


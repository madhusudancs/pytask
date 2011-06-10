#!/usr/bin/env python
#
# Copyright 2011 Authors of PyTask.
#
# This file is part of PyTask.
#
# PyTask is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyTask is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTask.  If not, see <http://www.gnu.org/licenses/>.


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    '"Nishanth Amuluru" <nishanth@fossee.in>',
    ]


import re

from django import forms

from pytask.taskapp.models import Task
from pytask.taskapp.models import TaskClaim
from pytask.taskapp.models import TaskComment
from pytask.taskapp.models import WorkReport


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

    def clean_tags_field(self):
        """Clean the tags field to contain only allowed characters.
        """
        tags_field = self.cleaned_data.get('tags_field', '')

        if tags_field and not re.match(r'[\w,\-&./\'\" ]+', tags_field):
            raise forms.ValidationError("Contains unallowed characters. "
              "Allowed characters are all alphabet, numbers, underscore(_), "
              "period(.), forward slash(/), dash(-), ampersand(&), single "
              "quote(') and space.")

        return tags_field

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

    def clean_tags_field(self):
        """Clean the tags field to contain only allowed characters.
        """
        tags_field = self.cleaned_data.get('tags_field', '')

        if tags_field and not re.match(r'[\w,\-&./\'\" ]+', tags_field):
            raise forms.ValidationError("Contains unallowed characters. "
              "Allowed characters are all alphabet, numbers, underscore(_), "
              "period(.), forward slash(/), dash(-), ampersand(&), single "
              "quote(') and space.")

        return tags_field

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
        fields = ['title', 'desc', 'pynts', 'tags_field']

    def clean_tags_field(self):
        """Clean the tags field to contain only allowed characters.
        """
        tags_field = self.cleaned_data.get('tags_field', '')

        if tags_field and not re.match(r'[\w,\-&./\'\" ]+', tags_field):
            raise forms.ValidationError("Contains unallowed characters. "
              "Allowed characters are all alphabet, numbers, underscore(_), "
              "period(.), forward slash(/), dash(-), ampersand(&), single "
              "quote(') and space.")

        return tags_field

class CreateChapterForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'desc' , 'pynts', 'tags_field']

    def clean_tags_field(self):
        """Clean the tags field to contain only allowed characters.
        """
        tags_field = self.cleaned_data.get('tags_field', '')

        if tags_field and not re.match(r'[\w,\-&./\'\" ]+', tags_field):
            raise forms.ValidationError("Contains unallowed characters. "
              "Allowed characters are all alphabet, numbers, underscore(_), "
              "period(.), forward slash(/), dash(-), ampersand(&), single "
              "quote(') and space.")

        return tags_field


class EditTextbookForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'desc', 'pynts', 'tags_field']

    def clean_tags_field(self):
        """Clean the tags field to contain only allowed characters.
        """

        tags_field = self.cleaned_data.get('tags_field', '')

        if tags_field and not re.match(r'^[\w,\-&./\'\" ]+$', tags_field):
            raise forms.ValidationError("Contains unallowed characters. "
              "Allowed characters are all alphabet, numbers, underscore(_), "
              "period(.), forward slash(/), dash(-), ampersand(&), single "
              "quote(') and space.")

        return tags_field


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


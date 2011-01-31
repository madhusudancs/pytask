"""Helper script that contains many utilities.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from tagging.managers import TaggedItem

from pytask.taskapp.models import Task


def remove_textbook_from_chapter():
    """Removes the tag Textbook from Chapter.
    """

    tasks = TaggedItem.objects.get_by_model(Task, 'Chapter')
    for task in tasks:
        tags = task.tags_field.split(',')
        retags = []
        for tag in tags:
            if 'Textbook' not in tag:
                retags.append(tag)
        task.tags_field = ', '.join(retags)
        task.save()

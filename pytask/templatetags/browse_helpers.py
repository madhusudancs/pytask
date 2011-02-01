"""Module containing the templatetags for rendering data especially for
browsing.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django import template


register = template.Library()


@register.inclusion_tag('templatetags/_as_browse_textbooks.html')
def as_list_tasks(tasks, title):
    """Returns a dictionary required to display the list of tasks.
    """

    return {
      'tasks': tasks,
      'title': title.capitalize(),
      }


@register.inclusion_tag('templatetags/_as_modification_display.html')
def as_modification_display(title, user, creation_datatime):
    """Returns a context dictionary containing the fields necessary
    to render the creation/modification.
    """

    return {
      'title': title,
      'user': user,
      'modification_datetime': creation_datatime,
      }


@register.inclusion_tag('templatetags/_as_uberbar.html')
def as_uberbar(message):
    """Returns a context dictionary containing the fields necessary
    to render the uberbar.
    """

    return {
      'message': message,
      }

"""Module containing the templatetags for rendering data especially for
browsing.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django import template


register = template.Library()


@register.inclusion_tag('templatetags/_as_browse_textbooks.html')
def as_list_textbooks(textbooks, title):
    """Returns a dictionary required to display the list of tasks.
    """

    return {
      'tasks': textbooks,
      'title': title,
      }


@register.inclusion_tag('templatetags/_as_div_field.html')
def as_div_field(field):
    """Returns the field for each div form field.
    """

    return {
      'field': field,
      }

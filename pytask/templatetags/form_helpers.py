"""Module containing the templatetags for constructing forms.
"""


__authors__ = [
    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
    ]


from django import template


register = template.Library()


@register.inclusion_tag('templatetags/_as_div_form.html')
def as_div_form(form, form_name, csrf_token, button_label,
                action_url='', file_support=False):
    """Returns a form to be constructed by the template specified.
    """

    return {
      'form': form,
      'form_name': form_name,
      'csrf_token': csrf_token,
      'action_url': action_url,
      'button_label': button_label,
      'file_support': file_support,
    }


@register.inclusion_tag('templatetags/_as_div_field.html')
def as_div_field(field):
    """Returns the field for each div form field.
    """

    return {
      'field': field,
      }

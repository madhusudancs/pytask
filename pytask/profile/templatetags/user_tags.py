from django import template

register = template.Library()

@register.filter
def notf_dsp(user):

    notf_cnt = user.notification_sent_to.filter(is_deleted=False,
                                                is_read=False).count()

    return u'Notifications(%s)'%notf_cnt if notf_cnt else u'Notifications'


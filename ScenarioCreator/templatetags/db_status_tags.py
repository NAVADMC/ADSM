__author__ = 'Josiah Seaman'

from django import template
from django.template.base import Node

register = template.Library()


@register.filter()
def active(target_address):
    if not target_address:  #TODO: Placeholder
        return 'active '
    return ''


@register.filter()
def completed(itemcount):
    if itemcount:
        return 'completed '
        # return 'class="completed "><span class="badge pull-right">%i</span' % len(itemcount)
    return ''


class FormCompleted(Node):
    def __init__(self, variable):
        self.queryset = variable

    def render(self, context):
        print(self.queryset)
        if self.queryset:
            return 'completed '
        return ''

@register.tag
def form_completed(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, queryset = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return FormCompleted(queryset)

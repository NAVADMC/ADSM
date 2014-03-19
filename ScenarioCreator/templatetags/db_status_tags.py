__author__ = 'Josiah Seaman'

from django import template
from django.template.base import Node

register = template.Library()


class FormCompleted(Node):
    def __init__(self, variable):
        self.queryset = variable

    def render(self, context):
        if len(self.queryset) > 0:
            return 'completed '
        return ''

@register.tag
def form_completed(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, queryset = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return FormCompleted(queryset[1:-1])

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
__author__ = 'Josiah Seaman'

from django import template
from django.template.base import Node
import re

register = template.Library()


@register.filter()
def active(target_address, url):
    if target_address.lower() in url.lower():
        return 'active '
    return ''


@register.filter()
def completed(itemcount):
    if itemcount:
        return 'completed '
        # return 'class="completed "><span class="badge pull-right">%i</span' % len(itemcount)
    return 'incomplete'


@register.filter()
def parent_link(model_link):
    return re.sub(r"/\d+/", '', model_link).replace(r"/new/", '')


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
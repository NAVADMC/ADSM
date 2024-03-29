from django.utils.safestring import mark_safe
from django import template
from django.template.base import Node
import re

register = template.Library()


@register.filter()
def active(target_address, url):
    if re.search(target_address, url, flags=re.IGNORECASE):
        return 'active '
    return ''


@register.filter()
def completed(itemcount):
    if itemcount:
        return 'completed'
        # return 'class="completed "><span class="badge pull-right">%i</span' % len(itemcount)
    return 'incomplete'


@register.filter()
def parent_link(model_link):
    return re.sub(r"/\d+/", '', model_link).replace(r"/new/", '')


@register.filter()
def action_id(action):
    return action.replace('/', '-')


@register.filter()
def wiki(words, url=None):
    """Wiki Definition: Generates a Lexicon link from a set of words with optional url help (when the titles don't match).  
    The call to wiki links is in the help text which is defined in ScenarioCreator.models file."""
    wiki_base = "https://github.com/NAVADMC/ADSM/wiki"
    lexicon = "/Lexicon-of-Disease-Spread-Modelling-terms#"  # pound sign
    if url is None:
        url = words.lower().replace(' ', '-')
        url = re.sub(r'[^\w-]', '', url)  # remove everything that's not a letter of hyphen
        url = wiki_base + lexicon + url
    elif url[:1] == '/':  # for linking wiki pages besides the Lexicon
        url = wiki_base + url
    elif url is not None:  # specific lexicon link that doesn't start with /
        url = wiki_base + lexicon + url
    return mark_safe('<a href="'+ url + '" class="wiki" target="_blank">' + words + '</a>')


def bold(words):
    return mark_safe('<strong>' + words + '</strong>')


def link(words, url):
    """Like the wiki filter above, but for external links"""
    return mark_safe('<a href="' + url + '" class="wiki" target="_blank">' + words + '</a>')


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

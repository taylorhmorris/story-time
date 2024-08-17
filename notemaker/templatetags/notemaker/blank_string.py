import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def blank_string(value, arg):
    compiled = re.compile(re.escape(arg), re.IGNORECASE)
    return compiled.sub('___', value)

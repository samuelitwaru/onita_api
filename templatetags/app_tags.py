from django import template
import random
from django.urls import reverse

register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.simple_tag
def random_number(min_value, max_value):
    return random.randint(min_value, max_value)


@register.simple_tag
def reverse_url(viewname, **kwargs):
    return reverse(viewname, kwargs=kwargs)
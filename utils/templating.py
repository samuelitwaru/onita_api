from jinja2 import Environment, FileSystemLoader

import os
import django
from django.middleware.csrf import get_token
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse
from django_middleware_global_request import get_request
# settings.configure(
#     TEMPLATES=[{
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.dirname(os.path.realpath(__file__))],  # script dir
#     }]
# )
django.setup()



jinja_env = Environment(loader=FileSystemLoader("templates/ajax"))
template = jinja_env.from_string("Hello, {{ name }}!")
template.render(name="World")

def render_template(template, context):
    context['reverse'] = reverse
    template = jinja_env.get_template('topic/topic_list.html')
    template.render(context)
    return template

def render_template(template, context):
    return render_to_string(
        template,
        context,
        request=get_request()
    )
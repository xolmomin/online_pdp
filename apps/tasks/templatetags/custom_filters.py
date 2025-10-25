from django import template
from django.template.defaultfilters import stringfilter
from django.utils.text import slugify

register = template.Library()

@register.filter
@stringfilter
def slugify_underscore(value):
    return slugify(value).replace("-", "_")

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def decode_utf8(value):
  return value.decode('UTF-8')
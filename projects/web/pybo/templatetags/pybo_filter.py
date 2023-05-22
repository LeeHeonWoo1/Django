from django import template
import math

register = template.Library()

@register.filter
def div(value, arg):
  res = value/arg
  result = math.ceil(res)
  return result

@register.filter
def sub(value, arg):
  return value-arg

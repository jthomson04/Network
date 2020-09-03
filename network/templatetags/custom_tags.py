from django import template
register = template.Library()
@register.filter(name='printvar')
def printvar(value):
    print(value)
    print(type(value))
    return ''

@register.filter(name='toStr')
def toStr(value):
    return str(value)

@register.simple_tag
def setvar(val=None):
  return val

@register.filter(name='index')
def index(value, arg):
    return value[arg]
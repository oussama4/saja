from django import template
 
from ..models import Menu

register = template.Library()

@register.simple_tag()
def get_menu(title):
    return Menu.objects.get(title=title)


@register.filter(name="split")
def split(value):
    return value.split('/')[1]

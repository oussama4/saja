from django import template

from ..models import Menu

register = template.Library()

@register.simple_tag()
def get_menu(title):
    return Menu.objects.get(title=title)


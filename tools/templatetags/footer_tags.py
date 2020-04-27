from django import template

from ..models import Footer

register = template.Library()



@register.simple_tag()
def get_footer(title):
    return Footer.objects.get(title=title)

from django import template

from wagtail.core.models import Page

from ..models import Menu

register = template.Library()


@register.simple_tag()
def catalog_menu():
    dump = Page.dump_bulk()
    brands = dump[0]['children'][0]['children']
    menu = []
    for b in brands:
        d = {'title': b['data']['title'], 'url': b['data']['url_path'], 'children': []}
        for c1 in b.get('children', []):
            d2 = {'title': c1['data']['title'], 'url': c1['data']['url_path'], 'children': []}
            for c2 in c1.get('children', []):
                if c2['data']['show_in_menus']:
                    d3 = {'title': c2['data']['title'], 'url': c2['data']['url_path'], 'children': []}
                    d2['children'].append(d3)
            d['children'].append(d2)
        menu.append(d)

    return menu


@register.simple_tag()
def get_menu(title):
    return Menu.objects.get(title=title)


@register.filter(name="split")
def split(value):
    return value.split('/')[1]

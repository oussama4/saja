from django import template

from wagtail.core.models import Page

from ..models import Menu
from catalog.models import Category
register = template.Library()


def reshape_url(url):
    l = url.split('/')[2:]
    return '/' + '/'.join(l)


@register.simple_tag()
def catalog_menu():
    dump = Page.dump_bulk()
    brands = dump[0]['children'][0]['children']
    menu = []
    ids = []
    for b in brands:
        if b['data']['show_in_menus']:
            d = {'title': b['data']['title'], 'url': reshape_url(b['data']['url_path']), 'children': []}
            for c1 in b.get('children', []):
                if c1['data']['show_in_menus']:
                    ids.append(c1['id'])
                    d2 = {'title': c1['data']['title'], 'url': reshape_url(c1['data']['url_path']), 'children': [],'id':c1['id']}
                    for c2 in c1.get('children', []):
                        if c2['data']['show_in_menus']:
                            d3 = {'title': c2['data']['title'], 'url': reshape_url(c2['data']['url_path']), 'children': []}
                            d2['children'].append(d3)
                    d['children'].append(d2)
            menu.append(d)
    categorys = Category.objects.filter(pk__in=ids)
    for item in menu:
        for i in item.get('children',[]):
            for c in categorys:
                if c.pk == i['id']:
                    i['color'] = c.color
    return menu


@register.simple_tag()
def get_menu(title):
    return Menu.objects.get(title=title)


@register.filter(name="split")
def split(value):
    return value.split('/')[1]

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Product


class ProductAdmin(ModelAdmin):
    model = Product
    menu_icon = 'placeholder'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('title', 'price', 'created')
    list_filter = ('')
    search_fields = ('title')

modeladmin_register(ProductAdmin)


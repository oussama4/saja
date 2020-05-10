from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Product


class ProductAdmin(ModelAdmin):
    model = Product
    menu_icon = 'placeholder'
    menu_order = 200
    add_to_settings_menu = False
    list_per_page = 50
    list_display = ('title', 'brand', 'category', 'price', 'created')
    list_filter = ('has_discount', 'product_range__brand', 'product_range__category')
    search_fields = ('title')
    inspect_view_enabled = True

modeladmin_register(ProductAdmin)


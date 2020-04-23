from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Order


class OrderAdmin(ModelAdmin):
    model = Order
    menu_icon = 'placeholder'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('user', 'status', 'total_price', 'payment_date')
    list_filter = ('status', 'user')

modeladmin_register(OrderAdmin)


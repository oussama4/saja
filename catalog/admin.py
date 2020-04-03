from wagtail.contrib.modeladmin.options import (
        ModelAdmin,
        modeladmin_register,
)

from .models import Category

@modeladmin_register
class CategorieAdmin(ModelAdmin):
    model = Category
    menu_order = 200
    add_to_settings_menu = False
    list_display = ("name", "brand", "parent", )
    list_filter = ("brand", "parent", )
    search_fields = ("name", )


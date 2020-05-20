from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register 
from .models import EmailSubscriber


class EmailSubscriber(ModelAdmin):
    model = EmailSubscriber
    menu_label = "emails"
    menu_icon = "mail"
    list_display = ("email","confirmed")
    list_filter = ("confirmed",)
    search_fields = ("email")
    
modeladmin_register(EmailSubscriber)

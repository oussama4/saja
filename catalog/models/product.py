from django.db import models
from django.utils.translation import gettext_lazy as _

#from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page

class Product(Page):
    
    product_title = models.CharField(
            verbose_name = _("titre"),
            blank=True,
            null=True,
            max_length=100
        )

 #   product_slug = AutoSlugField(populate_from="product_title", editable=True)

    product_image = models.ForeignKey(
            "wagtailimages.Image",
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
            help_text=_("image de produit")
        )
    product_price = models.FloatField(verbose_name=_("le prix"), blank=True,null=True)

    content_panels = Page.content_panels + [
            FieldPanel("product_title"),
#            FieldPanel("product_slug"),
            ImageChooserPanel("product_image"),
            FieldPanel("product_price"),
        ]

    class Meta:
        verbose_name = _("produit")
        verbose_name_plural = _("produits")



import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        MultiFieldPanel
)

class ProductImages(Orderable):
    product = ParentalKey(
            "catalog.Product",
            related_name="product_images",
    )
    product_image = models.ForeignKey(
            "wagtailimages.Image",
            verbose_name=_("image de produit"),
            related_name="+",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
    )

    panels = [
            ImageChooserPanel("product_image")
    ]

class Product(Page):
    subpage_types = ["catalog.Product"]

    description = RichTextField(
            verbose_name=_("description"),
            null=True,
            blank=True,
            features=["h2", "h4", "bold", "ol", "ul", "link"],
    )

    base_price = models.DecimalField(
            verbose_name=_("prix"),
            max_digits=7,
            decimal_places=2
    )
    has_discount = models.BooleanField(
            verbose_name=_("a une remise ?"),
            default=False
    )
    discount_percent = models.PositiveSmallIntegerField(
            verbose_name=_("pourcentage de remise"),
            default=20,
            validators=[MaxValueValidator(90)]
    )

    content_panels = Page.content_panels + [
            FieldPanel("description"),
            MultiFieldPanel(
                [
                    FieldPanel("base_price"),
                    FieldPanel("has_discount"),
                    FieldPanel("discount_percent"),
                ],
                heading=_("informations sur les prix"),
                classname="collapsible collapsed"
            ),
            InlinePanel("product_images", label="images de produit"),
    ]

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")

    @property
    def price(self):
        if self.has_discount:
            rest_percent = (100 - self.discount_percent) / 100
            discount_price = self.base_price * decimal.Decimal(rest_percent)
            return discount_price.quantize(decimal.Decimal('.00'))
        return self.base_price


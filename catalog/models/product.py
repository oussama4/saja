import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MaxValueValidator

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel

from wagtail.search import index
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import ListBlock, CharBlock
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
        FieldPanel,
        StreamFieldPanel,
        InlinePanel,
        MultiFieldPanel,
        PageChooserPanel,
        TabbedInterface,
        ObjectList,
)


class ProductBase(models.Model):
    """ abstract model for shared fields between product models and ranges """

    title = models.CharField(verbose_name=_("Titre"), max_length=150)
    slug = models.SlugField(unique=True)
    description = RichTextField(
            verbose_name=_("description"),
            null=True,
            blank=True,
            features=["h2", "h4", "bold", "ol", "ul", "link"],
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    panels = [
            FieldPanel("title"),
            FieldPanel("description"),
    ]

    class Meta:
        abstract = True


@register_snippet
class Attribute(models.Model):
    """ a product attribute like color, size, etc """

    name = models.CharField(verbose_name=_("Nom"), max_length=50)

    panels = [
            FieldPanel("name"),
    ]

    class Meta:
        verbose_name = _("attribut de produit")
        verbose_name_plural = _("attributs de produit")

    def __str__(self):
        return self.name

@register_snippet
class ProductRange(ProductBase):
    brand = models.ForeignKey(
            "catalog.Brand",
            verbose_name=_("marque"),
            related_name="ranges",
            on_delete=models.CASCADE
    )
    category = models.ForeignKey(
            "catalog.Category",
            verbose_name=_("categorie"),
            related_name="ranges",
            on_delete=models.CASCADE
    )
    range_image = models.ForeignKey(
            "wagtailimages.Image",
            verbose_name=_("image de gamme"),
            related_name="+",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
    )

    panels = ProductBase.panels + [
            PageChooserPanel("brand", "catalog.Brand"),
            PageChooserPanel("category", "catalog.Category"),
            ImageChooserPanel("range_image"),
    ]

    class Meta:
        verbose_name = _("Gamme")
        verbose_name_plural = _("Gammes")

    def __str__(self):
        return self.title


class ProductImages(Orderable):
    product = ParentalKey(
            "catalog.Product",
            related_name="product_images",
    )
    product_image = models.ForeignKey(
            "wagtailimages.Image",
            verbose_name=_("extrat image pour produit"),
            related_name="+",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
    )

    panels = [
            ImageChooserPanel("product_image")
    ]

class Product(ProductBase, index.Indexed, ClusterableModel):
    features = StreamField(
            [
                ("features", ListBlock(CharBlock(min_length=5, max_length=150)))
            ],
            verbose_name=_("caractéristique"),
            help_text=_("caractéristiques du produit"),
            blank=True,
            null=True
    )
    product_range = models.ForeignKey(
            ProductRange,
            verbose_name=_("gamme"),
            related_name="products",
            on_delete=models.CASCADE
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

    search_fields = [
            index.SearchField("title", partial_match=True, boost=2)
    ]

    panels = ProductBase.panels + [
            StreamFieldPanel("features"),
            SnippetChooserPanel("product_range")
    ]
    images_panels = [
            InlinePanel("product_images", label="images de produit"),
    ]
    price_panels = [
            MultiFieldPanel(
                [
                    FieldPanel("base_price"),
                    FieldPanel("has_discount"),
                    FieldPanel("discount_percent"),
                ],
                heading=_("informations sur les prix"),
            ),
    ]
    attribute_panels = [
            InlinePanel("attributes", label=_("attributs de produit"))
    ]

    edit_handler = TabbedInterface(
            [
                ObjectList(panels, heading=_('Contenu')),
                ObjectList(images_panels, heading=_('Images')),
                ObjectList(price_panels, heading=_('Prix')),
                ObjectList(attribute_panels, heading=_("Attributs de produit")),
            ]
    )

    class Meta:
        verbose_name = _("Produit")
        verbose_name_plural = _("Produits")
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        v = self.title
        if self.attributes:
            for attribute in self.attributes:
                v += attribute.value
        self.slug = slugify(v)
        super(Product, self).save(*args, **kwargs)

    @property
    def price(self):
        if self.has_discount:
            rest_percent = (100 - self.discount_percent) / 100
            discount_price = self.base_price * decimal.Decimal(rest_percent)
            return discount_price.quantize(decimal.Decimal('.00'))
        return self.base_price

    @property
    def first_image(self):
        return self.product_images.first()


class AttributeProduct(Orderable):
    """ intermediate model that assocaites a product with an attribute """

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name="attributes")
    value = models.CharField(verbose_name=_("valeur"), max_length=50, null=True, blank=True)

    panels = [
            SnippetChooserPanel("attribute"),
            FieldPanel("value")
    ]


from django.db import models
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
        FieldPanel,
        PageChooserPanel,
        TabbedInterface,
        ObjectList,
    )
from wagtail.images.edit_handlers import ImageChooserPanel

from colorfield.fields import ColorField
from .product import Product, ProductImages

class Category(Page):
    subpage_types = ["catalog.Category"]

    description = models.TextField(
            verbose_name=_("Description"),
            blank=True,
            null=True,
    )
    image = models.ForeignKey(
            "wagtailimages.Image",
            blank=True,
            null=True,
            related_name="+",
            on_delete=models.SET_NULL,
    )
    color = ColorField(default='#FFF')

    content_panels = Page.content_panels + [
            FieldPanel("description"),
            ImageChooserPanel("image"),
    ]

    color_panels = [FieldPanel('color')]

    edit_handler = TabbedInterface(
            [
                ObjectList(content_panels, heading=_("contenu")),
                ObjectList(color_panels, heading=_("couleur")),
                ObjectList(Page.promote_panels, heading=_("Promotion")),
                ObjectList(Page.settings_panels, heading=_("Paramètres")),
            ]
        )

    def get_context(self, request, *args, **kwargs):
            context = super().get_context(request, *args, **kwargs)

            descendant_categories = Category.objects.live().public().descendant_of(self)
            prefetch = Prefetch(
                lookup='product_images',
                queryset=ProductImages.objects.select_related('product_image'),
                to_attr='pimages'
            )
            products_qs = Product.objects.select_related('product_range__category').prefetch_related(prefetch)
            products = products_qs.filter(product_range__category=self)

            # if we're in a parent category
            subCat = []
            if descendant_categories:
                    subCat = descendant_categories
                    products = products_qs.filter(product_range__category__in=descendant_categories)

            # ordering
            order = request.GET.get("order", None)
            if order:
                if order == "title_asc":
                    products = products.order_by('title')
                elif order == "title_desc":
                    products = products.order_by('-title')
                elif order == "price_asc":
                    products = products.order_by('base_price')
                elif order == "price_desc":
                    products = products.order_by('-base_price')

            #pagination
            paginator = Paginator(products, 9)
            page = request.GET.get("page")

            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            context['products'] = products
            context['itemsSum'] = len(products)
            context['ancestors'] = self.get_ancestors(inclusive=True)[1:]
            context['categories'] = subCat
            context['color'] = self.color
            return context


    class Meta:
            verbose_name = _("Catégorie")
            verbose_name_plural = _("Catégories")

    def __str__(self):
            return self.title


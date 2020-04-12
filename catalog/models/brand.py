from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
        FieldPanel,
        InlinePanel,
        MultiFieldPanel,
        PageChooserPanel,
        StreamFieldPanel,
    )
from wagtail.core.fields import StreamField 
from wagtail.core.models import Page, Orderable 
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey 

from home import blocks 
from .product import Product
from .category import Category 

class CarouselBrandImage(Orderable):

    subpage_types = ["catalog.category"]

    brand = ParentalKey("catalog.brand", related_name = "carousel_images")
    carousel_image = models.ForeignKey(
            "wagtailimages.Image",
            null = True,
            blank = False,
            on_delete = models.SET_NULL,
            related_name = "+",
        )

    panels = [
            ImageChooserPanel("carousel_image"),
        ]


class GroupOfProducts(Orderable):
    
    brand = ParentalKey("catalog.Brand", related_name="group_products")
    
    group_product = models.ForeignKey(
            "Product",
            null=True,
            on_delete = models.SET_NULL,
            related_name = "+",
        )


    panels = [
            PageChooserPanel("group_product")
        ]


class Brand(RoutablePageMixin, Page):

    template = "catalog/brand.html"
    parent_page_types = ["home.Homepage"]
    subpage_types = ["catalog.category"]
        
    group_title = models.CharField(verbose_name=_("titre de groupe"), max_length= 100,null=True)
    
    body = StreamField(
            [
                (_("connect"),blocks.BrandConnect()),
                (_("paragraphe"),blocks.BrandParagraph()),
            ],
            null = True,
            blank = True,
       
        )
    
    content_panels = Page.content_panels + [
            InlinePanel("carousel_images", max_num=3, min_num=1, label = _("image")),
            MultiFieldPanel([
                FieldPanel("group_title"),
                InlinePanel("group_products", max_num=8, label = _("Meilleures Produits")),
        ],heading = _("choisir un groupe special de produit"),
          classname="collapsible collapsed",
        ),
            StreamFieldPanel("body")
    ]


    def get_context(self,request,*args,**kwargs):
        
        all_categories = Category.objects.live().public().descendant_of(self)
        filtred_cat = {}
        for item in all_categories:
            if item.get_parent().content_type == self.content_type:
                filtred_cat[item] = list(filter(lambda cat : item.title == cat.get_parent().title, all_categories))

        context = super().get_context(request, *args, **kwargs)
        context['categories'] = filtred_cat 
        context['ancestors'] = self.get_ancestors(inclusive=True)[1:]
        return context

    class Meta:
        verbose_name = _("Marque")
        verbose_name_plural = _("Marques")

    
    


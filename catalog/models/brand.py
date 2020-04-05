from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 
from django.utils.translation import gettext_lazy as _

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel 
from wagtail.core.models import Page, Orderable 
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey 

from .product import Product 

class CarouselBrandImage(Orderable):

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


class Brand(RoutablePageMixin, Page):

    template = "catalog/brand.html"
    subpage_types = ["catalog.category"]

    content_panels = Page.content_panels + [
            InlinePanel("carousel_images", max_num=3, min_num=1, label = _("image")),
        ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)
        all_products = Product.objects.live().public().order_by("-last_published_at").descendant_of(self)
        #pagination
        paginator = Paginator(all_products, 9)
        page = request.GET.get("page")
        
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products 
        context['itemsSum'] = len(all_products)
        context['ancestors'] = self.get_ancestors(inclusive=True)[1:]
        return context
    
    class Meta:
        verbose_name = _("Marque")
        verbose_name_plural = _("Marques")

    
    


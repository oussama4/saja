from django.db import models

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel 
from wagtail.core.models import Page, Orderable 
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey 


class CarouselImageBrand(Orderable):

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

    template = "brand/parent_band.html"

    custom_title = models.CharField(
            max_length = 100,
            blank = False,
            null = False,
            help_text = _("remplace le titre par defaut")
         )

    content_panels = Page.content_panels + [
            MultiFieldPanel([
                FieldPanel("custom_title"),
                ],heading = _("titre")
            ),
            InlinePanel("carousel_image", max_num=3, min_num=1, label = _("image")),
        ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)


    

    
    


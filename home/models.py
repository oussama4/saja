from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel, StreamFieldPanel

from home import blocks

class CarouselImages(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
            "wagtailimages.Image",
            null=True,
            blank=False,
            on_delete=models.SET_NULL,
            related_name="+",
    )

    panels= [
            ImageChooserPanel("carousel_image"),
    ]

class HomePage(Page):
    max_count = 1

    body = StreamField(
            [
                ("brands", blocks.BrandsBlock()),
            ],
            verbose_name=_("corps"),
            help_text=_("corps de page"),
            null=True,
            blank=True,
    )

    content_panels = Page.content_panels + [
            MultiFieldPanel(
                [
                    InlinePanel("carousel_images", max_num=5, min_num=1, label=_("Image")),
                ],
                heading=_("images de carrousel")
            ),
            StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = _("page d'accueil")
        verbose_name_plural = _("pages d'accueil")

    def get_admin_display_title(self):
        return _("Accueil")

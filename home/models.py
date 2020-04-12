from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
        InlinePanel,
        MultiFieldPanel,
        StreamFieldPanel,
        FieldPanel,
        PageChooserPanel,
)
from wagtail.snippets.models import register_snippet

from home import blocks

class CarouselImages(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
            "wagtailimages.Image",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name="+",
    )

    panels= [
            ImageChooserPanel("carousel_image"),
    ]

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 1

    body = StreamField(
            [
                ("brands", blocks.BrandsBlock()),
                ("connect", blocks.BrandConnect()),
            ],
            verbose_name=_("corps"),
            help_text=_("corps de page"),
            null=True,
            blank=True,
    )

    content_panels = Page.content_panels + [
            MultiFieldPanel(
                [
                    InlinePanel("carousel_images", max_num=5, min_num=0, label=_("Image")),
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

class MenuItem(Orderable):
    link_title = models.CharField(
            verbose_name=_("titre"),
            max_length=50,
    )
    link_page = models.ForeignKey(
            "wagtailcore.Page",
            related_name="+",
            verbose_name=_("page"),
            on_delete=models.CASCADE,
    )
    menu = ParentalKey(
            "home.Menu",
            related_name="menu_items",
            on_delete=models.CASCADE,
    )

    panels = [
            FieldPanel("link_title"),
            PageChooserPanel("link_page"),
    ]

    @property
    def title(self):
        return self.link_title

    @property
    def link(self):
        return self.link_page.url

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(
            verbose_name=_("titre"),
            max_length=50,
    )

    panels = [
            FieldPanel("title"),
            InlinePanel("menu_items", label=_("éléments de menu")),
    ]

    def __str__(self):
        return self.title


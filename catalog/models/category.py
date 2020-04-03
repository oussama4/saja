from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

class Category(Page):
    subpage_types = ["catalog.Product"]
    parent_page_types = ["catalog.Brand"]

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

    content_panels = Page.content_panels + [
            FieldPanel("description"),
            ImageChooserPanel("image"),
    ]

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    def __str__(self):
        return self.title


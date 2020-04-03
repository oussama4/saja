from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

class Category(models.Model):
    title = models.CharField(verbose_name=_("titre"), max_length=100)
    slug = models.SlugField()
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
    parent = models.ForeignKey(
            "self",
            blank=True,
            null=True,
            related_name="children",
            on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
            "catalog.Brand",
            verbose_name=_("Marque"),
            related_name="categories",
            on_delete=models.CASCADE,
    )

    panels = [
            FieldPanel("title"),
            FieldPanel("slug"),
            FieldPanel("description"),
            FieldPanel("parent"),
            ImageChooserPanel("image"),
            PageChooserPanel("brand"),
    ]

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    def __str__(self):
        return self.title


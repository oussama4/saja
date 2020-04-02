from django.db import models
from django.utils.translation import gettext_lazy as _

class Categorie(models.Model):
    name = models.CharField(verbose_name=_("Titre"), max_length=50)
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
            related_name="categories",
            on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("produit")
        verbose_name_plural = _("produits")

    def __str__(self):
        return self.title


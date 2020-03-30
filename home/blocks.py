from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class BrandsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("titre"), help_text=_("ajouter un titre"))
    brands = blocks.ListBlock(
            blocks.StructBlock(
                [
                    (_("image"), ImageChooserBlock(required=True)),
                    (_("titre"), blocks.CharBlock(max_length=100)),
                ]
            ),
            label=_("marques")
    )

    class Meta:
        template = "home/brands_block.html"
        icon = "placeholder"
        label = _("marques")


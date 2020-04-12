from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class BrandsBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("titre"), help_text=_("ajouter un titre"))
    brands = blocks.ListBlock(
            blocks.StructBlock(
                [
                    ("image", ImageChooserBlock(required=True)),
                    ("text", blocks.RichTextBlock(help_text=_("ajouter une paragraphe ici"))),
                ]
            ),
            label=_("marques")
    )

    class Meta:
        template = "home/home_paragraph.html"
        icon = "placeholder"
        label = _("marques")

class BrandConnect(blocks.StructBlock):

    media_title = blocks.CharBlock(required = True,max_length=60,help_text=_("le titre de paragraphe"))
    media_text = blocks.RichTextBlock(
            required = True,
            features=['h2', 'h3', 'bold', 'italic', 'link'],
            help_text=_("le paragraphe de  medias sociaux partie")
        )

    newsletter_title = blocks.CharBlock(required = True,max_length=50, help_text=_("le titre de NEWSLETTER"))
    newsletter_text = blocks.RichTextBlock(
            required = True,
            features = ['h2', 'h3', 'bold', 'italic', 'link'],
            help_text = _("le paragraphe de NEWSLETTER partie")
        )
    class Meta:
        template = "catalog/brand_connect.html"
        icon = "mail"
        label = _("Connect")


class BrandParagraph(blocks.StructBlock):

    title = blocks.CharBlock(required = True, max_length=50, help_text= _("le titre de paragraphe"))
    text = blocks.RichTextBlock(
            required = True,
            features= ['h2', 'h3', 'bold', 'italic', 'link'],
            help_text = _("le paragraphe de la marque")
        )
    image = ImageChooserBlock(required=False,help_text=_("image"))

    class Meta:
        template = "catalog/brand_paragraph.html"
        icon = "openquote"
        label = _("Paragraphe")





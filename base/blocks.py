from django.utils.translation import gettext_lazy as _

from wagtail.core.blocks import RichTextBlock, StructBlock, CharBlock


class TitleAndParagraphBlock(StructBlock):
    title = CharBlock(required=True, help_text=_("Titre de paragraphe"))
    paragraph = RichTextBlock(
            required = True,
            features= ['bold', 'italic', 'link'],
            help_text = _("le paragraphe")
        )

    class Meta:
        template = 'base/title_and_paragraph_block.html'
        icon = 'edit'
        label = _("Paragraphe avec titre")


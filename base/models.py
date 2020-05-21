from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from .blocks import TitleAndParagraphBlock

class StandardPage(Page):
    """ a generic content page """

    intro = models.TextField(
            blank=True,
            null=True,
            help_text = _("Texte pour décrire la page"),
    )
    body = StreamField(
            [
                ('paragraph', RichTextBlock(
                    ion = 'doc-full',
                    help_text = _("une paragraphe"),
                    features=["h2", "h4", "bold", "italic", "ol", "ul", "link"]
                )),
                ('title_and_paragraph', TitleAndParagraphBlock())
            ],
            verbose_name = _("corps"),
    )

    content_panels = Page.content_panels + [
            FieldPanel("intro"),
            StreamFieldPanel("body"),
    ]


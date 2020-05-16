from django.db import models

from anymail.message import AnymailMessage

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel 
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import (
        FieldPanel,
        MultiFieldPanel,
        InlinePanel,
        PageChooserPanel,
    )
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet

# Create your models here.

@register_setting
class MediasSociauxParametre(BaseSetting):

    facebook = models.URLField(blank=True, null=True, help_text="facebook url")
    instagram  = models.URLField(blank=True, null=True, help_text="tweeter url")
    youtube = models.URLField(blank=True, null=True, help_text="youtube url")

    panels =  [
        MultiFieldPanel([
                FieldPanel("facebook"),
                FieldPanel("instagram"),
                FieldPanel("youtube"),
            ],
            heading="médias sociaux"),
    ]


class FooterItem(Orderable):
    item_title =models.CharField(
            blank=True,
            null=True,
            max_length=60,
        )

    item_url = models.CharField(
            blank=True,
            max_length=500,
        )

    item_page = models.ForeignKey(
            "wagtailcore.Page",
            null=True,
            blank=True,
            related_name="+",
            on_delete=models.CASCADE,
        )
    
    item_footer = ParentalKey("Footer", related_name="footer_items")

    panels = [
            FieldPanel("item_title"),
            FieldPanel("item_url"),
            PageChooserPanel("item_page"),
        ]
    
    @property
    def title(self):
        if self.item_page and not self.item_title:
            return self.item_page.title
        elif self.item_title:
            return self.item_title
        else:
            return "pas de titre"


    @property
    def link(self):
        if self.item_page:
            return self.item_page.url 
        elif self.item_url:
            return self.item_url
        return "#"



@register_snippet 
class Footer(ClusterableModel):

    title = models.CharField(max_length=50)
    panels = [
            MultiFieldPanel([
                FieldPanel("title"),
                ],
            heading = "Footer"),
             InlinePanel("footer_items", label="Menu Item")

        ]

    def __str__(self):
        return self.title 
    
class EmailSubscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + "(" + ("Pas" if not self.confirmed else "")+ "confirmer)"

class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='newsletters/')

    def __str__(self):
        return self.subject+" "+ self.created_at.strftime("%B %d,%Y")
    
    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = EmailSubscriber.objects.filter(confirmed=True)
        for sub in subscribers:
            message = AnymailMessage(
                    subject = self.subject,
                    to = [sub.email],
                )
            content = contents+ f'<br><a href="{request.build_absolute_uri("/delete/")}?email={sub.email}&conf_num={sub.conf_num}">Unsubscribe</a>'
            message.attach_alternative(content,'text/html')
            message.send()





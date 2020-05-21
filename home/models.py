from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404 
from django.http import JsonResponse 
import random

from anymail.message import AnymailMessage

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
from wagtail.contrib.routable_page.models import RoutablePageMixin, route 
from catalog.models.brand import Brand 
from home import blocks
from tools.models import EmailSubscriber 
from tools.forms import EmailForm 

class CarouselImages(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
            "wagtailimages.Image",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name="+",
    )
    brand_page = models.ForeignKey(
            Brand,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+',
    )
    text = models.CharField(
            verbose_name= _("Phrase pour la Marque"),
            null=True,
            max_length=100,
    )
    logo =models.ForeignKey(
            "wagtailimages.Image",          
            null=True,         
            blank=True,        
            on_delete=models.SET_NULL,      
            related_name="+",  
    )


    panels= [
            ImageChooserPanel("carousel_image"),
            ImageChooserPanel("logo"),
            PageChooserPanel("brand_page"),
            FieldPanel("text"),
    ]


class HomePage(RoutablePageMixin, Page):
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


    def get_context(self, request):

        context = super().get_context(request)
        prefetch = models.Prefetch(
                'carousel_images',
                queryset=CarouselImages.objects.select_related('carousel_image', 'brand_page', 'logo'),
                to_attr='cimages'
        )

        context['form'] = EmailForm()
        context['home'] = HomePage.objects.prefetch_related(prefetch).live().public().get()
        return context

    @route(r'^send/$')
    def sendEmail(self, request):
        def random_digits():
            return "%0.12d" % random.randint(0, 999999999999)
        message = ""
        if request.method == "POST" :
            form = EmailForm(request.POST)
            if form.is_valid():
                try:
                    sub = EmailSubscriber.objects.get(email = request.POST['email'])
                    message = f'{sub.email} existe déjà'
                except ObjectDoesNotExist:
                    sub = EmailSubscriber(email=request.POST['email'],conf_num =random_digits())
                    sub.save()
                    message = AnymailMessage(
                            subject='Newsletter confirmation',
                            to = [sub.email],
                    )
                    message.attach_alternative(f"confirm your subscribtion by entering<a href='{request.build_absolute_uri('/confirm/')}?email={sub.email}&conf_num={sub.conf_num}'>this link</a>",'text/html')
                    message.send()
                    message = f'Nous vous avons envoyé un e-mail de confirmation à {sub.email}'
            else:
                message = 'Entrer un email valide'
            return JsonResponse({"message":message})
        
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


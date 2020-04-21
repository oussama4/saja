from django.db import models
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from .product import Product, ProductImages 

class Category(Page):
    subpage_types = ["catalog.Product", "catalog.Category"]

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

    def get_context(self, request, *args, **kwargs):

            context = super().get_context(request, *args, **kwargs)
            descendant_categories = Category.objects.live().public().descendant_of(self)
            prefetch = Prefetch(
                lookup='product_images',
                queryset=ProductImages.objects.select_related('product_image'),
                to_attr='pimages'
            )
            all_products = Product.objects.prefetch_related(prefetch).live().public().order_by("-last_published_at").descendant_of(self)
            
            subCat = []
            if descendant_categories:
                    subCat = descendant_categories 

            #brandCat = None 
            #if self.get_parent().content_type == self.content_type:
            #    brandCat = all_categories.descendant_of(self.get_parent().get_parent())
            #else:
            #    brandCat = all_categories.descendant_of(self.get_parent())

            #filtred_cat = {}
        
            #for item in brandCat:
            #    if not item.get_parent().content_type == self.content_type:
            #        filtred_cat[item] = list(filter(lambda cat : item.title == cat.get_parent().title, brandCat))


            #pagination
            paginator = Paginator(all_products, 12)
            page = request.GET.get("page")
            
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            context['products'] = products 
            context['itemsSum'] = len(all_products)
            context['ancestors'] = self.get_ancestors(inclusive=True)[1:]
            context['categories'] = subCat 
            return context


    class Meta:
            verbose_name = _("Catégorie")
            verbose_name_plural = _("Catégories")

    def __str__(self):
            return self.title


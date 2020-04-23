from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from .models import Product, ProductImages

def product(request, slug):
    prefetch = Prefetch(
        lookup='product_images',
        queryset=ProductImages.objects.select_related('product_image'),
        to_attr='pimages'
    )
    p = get_object_or_404(Product.objects.prefetch_related(prefetch), slug=slug)
    return render(request, "catalog/product.html", {'product': p})


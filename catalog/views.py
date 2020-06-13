from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Product, ProductImages

def product(request, slug):
    prefetch = Prefetch(
        lookup='product_images',
        queryset=ProductImages.objects.select_related('product_image'),
        to_attr='pimages'
    )
    p = get_object_or_404(Product.objects.select_related('product_range').prefetch_related(prefetch), slug=slug)
    v = Product.objects.prefetch_related(prefetch).filter(product_range=p.product_range).exclude(pk=p.pk).all()
    return render(request, "catalog/product.html", {'product': p, 'variants': v})


def promotions(request):
    prefetch = Prefetch(
        lookup='product_images',
        queryset=ProductImages.objects.select_related('product_image'),
        to_attr='pimages'
    )
    promoted_products = Product.objects.prefetch_related(prefetch).filter(has_discount=True)

    # pagination
    paginator = Paginator(promoted_products, 9)
    # Try to get the ?page=x value
    page = request.GET.get("page")
    try:
        # If the page exists and the ?page=x is an int
        products = paginator.page(page)
    except PageNotAnInteger:
        # If the ?page=x is not an int; show the first page
        products = paginator.page(1)
    except EmptyPage:
        # If the ?page=x is out of range (too high most likely)
        # Then return the last page
        products = paginator.page(paginator.num_pages)

    return render(request, "catalog/promotions.html", {'products': products})


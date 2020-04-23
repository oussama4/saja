from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.db.models import Prefetch

from wagtail.core.models import Page
from wagtail.search.models import Query
from wagtail.search.backends import get_search_backend

from catalog.models import Product, ProductImages


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        s = get_search_backend(backend='pgfts')
        prefetch = Prefetch(
                lookup='product_images',
                queryset=ProductImages.objects.select_related('product_image'),
                to_attr='pimages'
        )
        search_results = s.search(search_query, Product.objects.prefetch_related(prefetch))
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Product.objects.none()

    # Pagination
    paginator = Paginator(search_results, 12)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        'results_count': len(search_results),
    })

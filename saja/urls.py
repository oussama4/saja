from django.conf import settings 
from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views import generic as generic_views

from wagtail.images.views.serve import ServeView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from users import views as users_views
from catalog import views as catalog_views

urlpatterns = [
    url(r'^django-codylia-2020/', admin.site.urls),

    url(r'^codylia-2020/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include('allauth.urls')),
    url(r'', include('checkout.urls',namespace='checkout')),

    url(r'^search/$', search_views.search, name='search'),
    # url(r'^signup/$', users_views.SignUp.as_view(), name='signup'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^profile/address/create/$', users_views.create_address, name='address_create'),
    path('profile/address/change/<int:pk>', users_views.ChangeAddress.as_view(), name='address_change'),
    path('profile/info/change/<int:pk>', users_views.UserUpdate.as_view(), name='info_change'),
    path('profile/orders', users_views.OrdersList.as_view(), name='orders_list'),
    path('<slug:slug>', catalog_views.product, name='product_detail'),
    url(r'^profile/address/$',
        generic_views.TemplateView.as_view(template_name='users/address.html'),
        name='address'),
    url(r'^profile/$', users_views.profile, name='profile'),
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),
    url(r'', include(wagtail_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # debug toolbar
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns


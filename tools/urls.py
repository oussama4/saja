from django.urls import path
from .views import new, confirm 


urlpatterns = [
    path('new/', new, name = 'new'),
    path('confirm/', confirm, name = 'confirm'),
]

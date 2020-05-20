from django.urls import path
from .views import new, confirm, delete  


urlpatterns = [
    path('confirm/', confirm, name = 'confirmEmail'),
    path('delete/', delete, name = 'deleteEmail'),
]

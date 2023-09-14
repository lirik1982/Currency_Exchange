from django.urls import path
from .views import exchange, exchange_api

urlpatterns = [
    path('api/rates', exchange_api),
    path('', exchange, name='exchange'),
]

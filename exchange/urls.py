from django.urls import path
from .views import Main, exchange_api

urlpatterns = [
    path('api/rates', exchange_api),
    path('', Main.as_view(), name='exchange'),
]

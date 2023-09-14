from django.urls import path
from .views import Main, ResponseAPI

urlpatterns = [
    path('api/rates', ResponseAPI.as_view()),
    path('', Main.as_view(), name='exchange'),
]

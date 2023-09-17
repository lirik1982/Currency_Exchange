from django.urls import path
from .views import Main
from .views_API import ResponseAPI

urlpatterns = [
    path('api/rates', ResponseAPI.as_view()),
    path('', Main.as_view(), name='exchange'),
]

# filepath: /Users/abhinavjain/Zephyra/zephyra_backend/mynewapp/urls.py
from django.urls import path
from .views import generate_aes_key, my_view

urlpatterns = [
    path('my-endpoint/', my_view, name='my-endpoint'),
    path('generate-aes-key/', generate_aes_key, name='generate-aes-key'),
]
from django.urls import path
from .views import ContactoCreateView

urlpatterns = [
    path('contacto/', ContactoCreateView.as_view(), name='contacto'),
]
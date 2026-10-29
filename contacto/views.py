from rest_framework import generics
from .models import Mensaje
from .serializers import MensajeSerializer


class ContactoCreateView(generics.CreateAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
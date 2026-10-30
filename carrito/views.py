from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Carrito, ItemCarrito
from .serializers import CarritoSerializer, ItemCarritoSerializer


class CarritoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_carrito(self, request):
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        return carrito

    def list(self, request):
        carrito = self._get_carrito(request)
        return Response(CarritoSerializer(carrito).data)

    @action(detail=False, methods=['post'])
    def agregar(self, request):
        carrito = self._get_carrito(request)
        serializer = ItemCarritoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data.get('cantidad', 1)

        item = carrito.items.filter(producto=producto).first()
        total = cantidad + (item.cantidad if item else 0)
        if total > producto.stock:
            return Response(
                {'cantidad': [f'Solo hay {producto.stock} unidades disponibles.']},
                status=400
            )

        if item:
            item.cantidad = total
            item.save()
        else:
            ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

        return Response(CarritoSerializer(carrito).data, status=201)

    @action(detail=False, methods=['delete'])
    def vaciar(self, request):
        carrito = self._get_carrito(request)
        carrito.items.all().delete()
        return Response(CarritoSerializer(carrito).data, status=200)


class ItemCarritoViewSet(mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ItemCarritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemCarrito.objects.filter(carrito__usuario=self.request.user)
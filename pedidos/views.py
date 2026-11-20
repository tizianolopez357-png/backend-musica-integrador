from django.db import transaction
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carrito.models import Carrito
from productos.models import Producto
from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer


class PedidoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).prefetch_related('items__producto')

    @action(detail=False, methods=['post'])
    def finalizar(self, request):
        try:
            with transaction.atomic():
                carrito = Carrito.objects.select_for_update().get(usuario=request.user)
                items = list(carrito.items.select_for_update().select_related('producto'))

                if not items:
                    return Response(
                        {'detail': 'El carrito está vacío.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                pedido = Pedido.objects.create(usuario=request.user)

                for item in items:
                    producto = Producto.objects.select_for_update().get(pk=item.producto_id)
                    if item.cantidad > producto.stock:
                        raise StockInsuficiente(
                            f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}'
                        )

                    ItemPedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item.cantidad,
                        precio_unitario=producto.precio,
                    )
                    producto.stock -= item.cantidad
                    producto.save(update_fields=['stock'])

                carrito.items.all().delete()

            pedido.refresh_from_db()
            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

        except Carrito.DoesNotExist:
            return Response(
                {'detail': 'El carrito no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except StockInsuficiente as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class StockInsuficiente(Exception):
    pass

# Create your views here.

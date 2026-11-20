from rest_framework import serializers
from .models import Carrito, ItemCarrito


class ItemCarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    precio_unitario = serializers.DecimalField(
        source='producto.precio', max_digits=10, decimal_places=2, read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'producto_nombre', 'precio_unitario', 'cantidad', 'subtotal']
        read_only_fields = ['id']

    def get_subtotal(self, obj):
        return obj.cantidad * obj.producto.precio

    def validate(self, data):
        producto = data.get('producto')
        if self.instance:
            producto = producto or self.instance.producto
            cantidad = data.get('cantidad', self.instance.cantidad)
        else:
            cantidad = data.get('cantidad', 1)

        if producto is None:
            raise serializers.ValidationError({'producto': 'Este campo es obligatorio.'})
        if cantidad < 1:
            raise serializers.ValidationError({'cantidad': 'La cantidad debe ser al menos 1.'})
        if cantidad > producto.stock:
            raise serializers.ValidationError(
                {'cantidad': f'Solo hay {producto.stock} unidades disponibles.'}
            )
        return data


class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'items', 'total']

    def get_total(self, obj):
        return sum(item.cantidad * item.producto.precio for item in obj.items.all())
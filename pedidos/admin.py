from django.contrib import admin

from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['precio_unitario']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'estado', 'creado']
    list_filter = ['estado', 'creado']
    search_fields = ['usuario__username', 'usuario__email']
    inlines = [ItemPedidoInline]

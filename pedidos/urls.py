from rest_framework.routers import SimpleRouter

from .views import PedidoViewSet

router = SimpleRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedidos')

urlpatterns = router.urls

from rest_framework.routers import SimpleRouter
from .views import CarritoViewSet, ItemCarritoViewSet

router = SimpleRouter()
router.register(r'carrito', CarritoViewSet, basename='carrito')
router.register(r'items', ItemCarritoViewSet, basename='items')

urlpatterns = router.urls

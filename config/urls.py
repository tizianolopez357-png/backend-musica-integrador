from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@api_view(['GET'])
def api_root(request):
    return Response({
        'productos': reverse('producto-list', request=request),
        'categorias': reverse('categoria-list', request=request),
        'carrito': reverse('carrito-list', request=request),
        'pedidos': reverse('pedidos-list', request=request),
        'contacto': reverse('contacto', request=request),
        'token': reverse('token_obtain_pair', request=request),
    })


urlpatterns = [
    path('', lambda request: redirect('/api/'), name='inicio'),
    path('api/', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('productos.urls')),
    path('api/', include('contacto.urls')),
    path('api/', include('carrito.urls')),
    path('api/', include('pedidos.urls')),
]
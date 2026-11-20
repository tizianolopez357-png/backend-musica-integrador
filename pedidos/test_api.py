from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from productos.models import Categoria, Producto


class APIFlowsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='comprador', password='clave123')
        self.categoria = Categoria.objects.create(nombre='Guitarras')
        self.producto = Producto.objects.create(
            nombre='Guitarra Test', descripcion='Instrumento de prueba',
            imagen='https://example.com/guitarra.jpg', marca='Test',
            precio='100.00', stock=5, categoria=self.categoria,
        )

    def autenticar(self):
        response = self.client.post('/api/token/', {'username': 'comprador', 'password': 'clave123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_unauthenticated_cart_requires_login(self):
        response = self.client.get('/api/carrito/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_list_supports_filters_and_search(self):
        response = self.client.get('/api/productos/?search=Guitarra&precio_gte=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_add_to_cart(self):
        self.autenticar()
        response = self.client.post('/api/carrito/agregar/', {'producto': self.producto.id, 'cantidad': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['items'][0]['cantidad'], 2)
        self.assertEqual(str(response.data['total']), '200.00')

    def test_cannot_add_more_than_stock(self):
        self.autenticar()
        response = self.client.post('/api/carrito/agregar/', {'producto': self.producto.id, 'cantidad': 6}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_discounts_stock_and_clears_cart(self):
        self.autenticar()
        self.client.post('/api/carrito/agregar/', {'producto': self.producto.id, 'cantidad': 2}, format='json')
        response = self.client.post('/api/pedidos/finalizar/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 3)

        carrito = self.client.get('/api/carrito/')
        self.assertEqual(carrito.data['items'], [])

    def test_user_cannot_view_another_users_orders(self):
        self.autenticar()
        other = User.objects.create_user(username='otro', password='clave123')
        from pedidos.models import Pedido
        Pedido.objects.create(usuario=other)
        response = self.client.get('/api/pedidos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

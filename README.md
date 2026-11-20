# API Tienda de Música

## Instalación

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata productos.json
python manage.py createsuperuser
python manage.py runserver
```

## Autenticación

Usar JWT: `POST /api/token/` con `username` y `password`. Enviar el access token como `Authorization: Bearer <token>`.

## Endpoints

| Método | Ruta | Descripción | Auth | Cuerpo | Respuesta ejemplo |
|---|---|---|---|---|---|
| POST | `/api/token/` | Obtener tokens JWT | No | `{"username":"usuario","password":"clave"}` | `{"access":"...","refresh":"..."}` |
| POST | `/api/token/refresh/` | Renovar access token | No | `{"refresh":"..."}` | `{"access":"..."}` |
| GET | `/api/categorias/` | Listar categorías | No | — | `[{"id":1,"nombre":"Guitarras"}]` |
| GET | `/api/productos/` | Listar y filtrar productos | No | — | `{"count":10,"results":[...]}` |
| POST | `/api/productos/` | Crear producto | Admin | Datos del producto | Producto creado |
| GET | `/api/carrito/` | Ver carrito del usuario | Sí | — | `{"id":1,"items":[],"total":"0"}` |
| POST | `/api/carrito/agregar/` | Agregar producto | Sí | `{"producto":1,"cantidad":2}` | Carrito actualizado |
| PATCH | `/api/items/{id}/` | Cambiar cantidad | Sí | `{"cantidad":3}` | Ítem actualizado |
| DELETE | `/api/items/{id}/` | Eliminar ítem | Sí | — | 204 |
| DELETE | `/api/carrito/vaciar/` | Vaciar carrito | Sí | — | Carrito vacío |
| POST | `/api/pedidos/finalizar/` | Crear pedido desde carrito | Sí | `{}` | Pedido creado con items y total |
| GET | `/api/pedidos/` | Historial del usuario | Sí | — | Lista de pedidos propios |
| GET | `/api/pedidos/{id}/` | Detalle propio | Sí | — | Pedido con items |
| POST | `/api/contacto/` | Enviar mensaje | No | `{"nombre":"Ana","correo":"ana@mail.com","mensaje":"Consulta larga"}` | Mensaje creado |

Los filtros disponibles en productos incluyen `categoria`, `precio_gte`, `precio_lte`, `search` y `ordering`.

## Pruebas

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py test pedidos.test_api
```

La compra usa `transaction.atomic()` para que la creación del pedido, la actualización de stock y el vaciado del carrito sean una única operación. Si falla el stock o ocurre un error, se revierten todos los cambios.

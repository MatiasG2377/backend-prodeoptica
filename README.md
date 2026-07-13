# REST_API_OPTICA

API REST para gestión de inventario, ventas y usuarios de una óptica (multi-sucursal). Construida con Django + Django REST Framework, autenticación JWT.

## Stack

- Django 5.1, Django REST Framework
- PostgreSQL
- Autenticación: `djangorestframework-simplejwt` (access/refresh tokens, blacklist en logout)
- Variables de entorno: `django-environ`
- Tests: `pytest-django`

## Setup local

```bash
cd REST_API_OPTICA
python -m venv ../venv          # si no existe ya
../venv/Scripts/pip install -r requirements.txt

cp .env.example .env             # completar con tus credenciales de Postgres
                                  # generar SECRET_KEY:
                                  # python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Corre en `REST_API_OPTICA.settings.dev` por defecto (ver `manage.py`). Para producción, la variable de entorno `DJANGO_SETTINGS_MODULE=REST_API_OPTICA.settings.prod` sobreescribe eso — ver `REST_API_OPTICA/settings/prod.py` para lo que cambia (`DEBUG=False`, cookies seguras, `ALLOWED_HOSTS` sin default).

## Tests

```bash
python -m pytest REST_API_OPTICA/inventario/tests.py -v
```

## Estructura

```
REST_API_OPTICA/                    # carpeta del proyecto Django (manage.py vive acá)
  REST_API_OPTICA/                  # paquete de configuración (settings/, urls.py, wsgi.py, asgi.py)
    settings/
      base.py                      # settings comunes (lee de .env vía django-environ)
      dev.py                       # override: DEBUG=True, cookies no-seguras
      prod.py                      # override: DEBUG=False, cookies seguras, HTTPS
  inventario/                      # app Django única (el dominio es cohesivo, no se dividió en múltiples apps)
    models/
      usuarios.py                  # User (custom), Sucursal
      inventario.py                # Categoria, Producto, Proveedor, ProductoProveedor, MovimientoInventario, Lote
      ventas.py                    # Cliente, Venta, ArticuloVenta
    services.py                    # lógica de negocio que escribe/muta datos (ej. crear_usuario)
    selectors.py                   # queries de solo lectura reusables (ej. buscar_productos)
    API/
      views/                       # mismo split por dominio que models/
      serializers/                 # ídem
      permissions.py               # IsAdministrador, IsGerente, IsUsuario, IsAdminOrManager
      JWT/                         # rutas de login/refresh/logout/register
      urls.py                      # router DRF
    tests.py
```

## Decisiones de arquitectura

- **Una sola app Django (`inventario`)**: los modelos (usuarios, inventario, ventas) comparten el mismo bounded context — dividir en apps separadas ahora sería sobre-ingeniería sin necesidad real de desplegar/escalar cada dominio por separado.
- **Split por dominio dentro de cada capa** (`models/`, `API/views/`, `API/serializers/`): mismo mapa mental en las tres capas (buscás "ventas" y sabés qué archivo tocar en cualquiera). Cada paquete tiene un `__init__.py` que reexporta todo, así el resto del código importa igual que si fuera un solo archivo.
- **`services.py` / `selectors.py`**: separan lógica de negocio (escritura) y queries (lectura) de las views/serializers, que quedan finos. Patrón tomado del [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).
- **Roles y permisos**: `User.rol` (`Administrador`/`Gerente`/`Usuario`) + permission classes custom (`inventario/API/permissions.py`). `UserViewSet` restringido a `IsAdminOrManager` — solo admins/gerentes pueden gestionar otros usuarios.
- **Settings por entorno**: `base.py` (común) + `dev.py`/`prod.py` (override), todo secreto vía variables de entorno (`.env`, nunca commiteado).

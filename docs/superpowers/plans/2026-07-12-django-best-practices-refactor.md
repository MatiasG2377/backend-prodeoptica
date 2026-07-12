# REST_API_OPTICA — Refactor a Buenas Prácticas Django (Portfolio-Grade) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Llevar REST_API_OPTICA de un prototipo funcional a un ejemplo de portafolio limpio: sin secretos filtrados, sin repo hinchado, con convenciones Django estándar, permisos correctos y tests reales.

**Architecture:** Se mantiene 1 proyecto Django + 1 app `inventario` (el dominio es cohesivo: óptica con inventario/ventas/usuarios comparten el mismo bounded context — dividir en múltiples apps ahora sería sobre-ingeniería). Se introduce: settings por entorno vía `django-environ`, capa de tests con `pytest-django`, y limpieza de nombres de archivo a convención Django (`views.py`, `urls.py`, `serializers.py`).

**Tech Stack:** Django 5.1, DRF, SimpleJWT, django-environ, pytest-django, PostgreSQL.

## Global Constraints

- No romper URLs públicas existentes (`/api/categorias/`, `/api/productos/`, etc.) — mismo `basename` y paths.
- No perder datos de `db.sqlite3` real de producción/dev si el usuario lo necesita — se hace backup antes de sacarlo de git, no se borra el archivo local.
- Todo commit debe dejar el proyecto arrancando (`python manage.py check` sin errores).
- Mantener nombres de campos de modelo en español (dominio ya establecido, migraciones existentes dependen de esto) — NO renombrar columnas de modelos en este plan, solo lo explícitamente listado (fix de typo puntual).

---

## Fase 0 — Higiene de repo (crítico, hacer primero)

### Task 1: `.gitignore` + sacar `venv/` y `db.sqlite3` del control de versiones

**Files:**
- Create: `.gitignore`
- Modify: git index (untrack, no borra archivos locales)

**Interfaces:** ninguna (no afecta código Python).

- [ ] **Step 1: Crear `.gitignore`**

```gitignore
# Entornos virtuales
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]
*.egg-info/

# Django
*.sqlite3
/staticfiles/
/media/

# Secrets
.env

# IDE
.idea/
.vscode/
```

- [ ] **Step 2: Backup de la base local antes de destrackearla**

```bash
cp REST_API_OPTICA/db.sqlite3 REST_API_OPTICA/db.sqlite3.bak
```

- [ ] **Step 3: Destrackear venv y sqlite del índice de git (sin borrar del disco)**

```bash
git rm -r --cached venv
git rm --cached REST_API_OPTICA/db.sqlite3
```

- [ ] **Step 4: Verificar que git status ya no los liste como tracked y que siguen en disco**

```bash
git status
ls venv/Scripts/python.exe
ls REST_API_OPTICA/db.sqlite3
```

Expected: `venv/` y `db.sqlite3` aparecen como "deleted" (staged) en git status, pero los archivos siguen existiendo en disco.

- [ ] **Step 5: Commit**

```bash
git add .gitignore
git commit -m "chore: stop tracking venv and sqlite3, add .gitignore"
```

### Task 2: `requirements.txt` reproducible

**Files:**
- Create: `REST_API_OPTICA/requirements.txt`

**Interfaces:** ninguna.

- [ ] **Step 1: Generar el archivo desde el venv activo**

```bash
venv/Scripts/pip.exe freeze > REST_API_OPTICA/requirements.txt
```

- [ ] **Step 2: Revisar que incluya al menos:** `Django==5.1.3`, `djangorestframework`, `djangorestframework-simplejwt`, `django-cors-headers`, `django-extensions`, `psycopg2-binary` (o el driver postgres que uses). Si falta alguno porque no estaba instalado nombrado exactamente así, agregarlo a mano con la versión instalada.

- [ ] **Step 3: Commit**

```bash
git add REST_API_OPTICA/requirements.txt
git commit -m "chore: add requirements.txt for reproducible installs"
```

---

## Fase 1 — Seguridad (crítico)

### Task 3: Mover secretos a variables de entorno con `django-environ`

**Files:**
- Modify: `REST_API_OPTICA/REST_API_OPTICA/settings.py:19-38, 114-123`
- Create: `REST_API_OPTICA/.env`
- Create: `REST_API_OPTICA/.env.example`

**Interfaces:**
- Consumes: ninguna
- Produces: `env` object disponible en `settings.py` para futuras fases (Task 12, settings split, lo reusa)

- [ ] **Step 1: Instalar django-environ**

```bash
venv/Scripts/pip.exe install django-environ
venv/Scripts/pip.exe freeze > REST_API_OPTICA/requirements.txt
```

- [ ] **Step 2: Crear `REST_API_OPTICA/.env`** (NO se commitea, ya está en `.gitignore`)

```env
DEBUG=True
SECRET_KEY=django-insecure-up^qzr@vps#xy#k*hw)no@5w%yaxs-g^$-m&p8b9*n9d0-yy^w
DB_NAME=inventario
DB_USER=postgres
DB_PASSWORD=Passw3rd+
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

- [ ] **Step 3: Crear `REST_API_OPTICA/.env.example`** (SÍ se commitea, es la plantilla pa' cualquiera que clone el repo)

```env
DEBUG=True
SECRET_KEY=change-me-generate-a-new-one
DB_NAME=inventario
DB_USER=postgres
DB_PASSWORD=change-me
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

- [ ] **Step 4: Editar `settings.py` líneas 13-40** — reemplazar:

```python
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECURE_SSL_REDIRECT = False  # Redirige todas las solicitudes HTTP a HTTPS
SESSION_COOKIE_SECURE = False  # Solo enviar cookies de sesión a través de HTTPS
CSRF_COOKIE_SECURE = False  # Solo enviar cookies CSRF a través de HTTPS


SECURE_HSTS_SECONDS = 0  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False


CORS_ALLOW_ALL_ORIGINS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-up^qzr@vps#xy#k*hw)no@5w%yaxs-g^$-m&p8b9*n9d0-yy^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
```

por:

```python
from pathlib import Path
from datetime import timedelta
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = not env.bool('DEBUG', default=False)
CSRF_COOKIE_SECURE = not env.bool('DEBUG', default=False)

SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

- [ ] **Step 5: Editar `settings.py` líneas 114-123 (bloque `DATABASES`)** — reemplazar:

```python
DATABASES = {
    'default': {        
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventario',
        'USER': 'postgres',  # Uso de la conexión
        'PASSWORD': 'Passw3rd+',  # Contraseña de la conexión
        'HOST': 'localhost',  # Hostname o IP del servidor PostgreSQL
        'PORT': 5432  # Porta que tu programa tiene habilitada para la conexión a PostgreSQL.
    }
}
```

por:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env.int('DB_PORT', default=5432),
    }
}
```

- [ ] **Step 6: Verificar que el proyecto sigue arrancando**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py check
```

Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 7: Commit**

```bash
git add REST_API_OPTICA/REST_API_OPTICA/settings.py REST_API_OPTICA/.env.example REST_API_OPTICA/requirements.txt
git commit -m "fix: move secrets to environment variables via django-environ"
```

> Nota: `SECRET_KEY` actual quedó expuesta en el historial de git de todas formas. Si el repo es público, regenerar una nueva con `django.core.management.utils.get_random_secret_key()` y rotarla en `.env` (no hace falta commitear nada, `.env` no se trackea).

### Task 4: Arreglar permisos de `UserViewSet` (escalación de privilegios)

**Problema real:** `settings.py` define `DEFAULT_PERMISSION_CLASSES: [IsAuthenticated]`. `UserViewSet` (vistas.py:55-57) no sobreescribe permisos → **cualquier usuario autenticado, sin importar rol, puede crear/editar/eliminar cualquier otro usuario vía `/api/user/`**, incluyendo asignarse rol `Administrador`. Esto contradice el propósito de `RegisterView` que sí restringe a admin/gerente.

**Files:**
- Modify: `REST_API_OPTICA/inventario/API/vistas.py:55-57`

**Interfaces:**
- Consumes: `IsAdminOrManager` de `inventario.API.permissions` (ya importado en el archivo, línea 14)
- Produces: ninguno nuevo

- [ ] **Step 1: Editar vistas.py líneas 55-57** — reemplazar:

```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

por:

```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
```

- [ ] **Step 2: Probar manualmente con un usuario rol 'Usuario' autenticado**

```bash
# Con token de un usuario rol=Usuario en el header Authorization: Bearer <token>
curl -X GET http://localhost:8000/api/user/ -H "Authorization: Bearer <token_usuario_normal>"
```

Expected: `403 Forbidden` (antes del fix daba `200 OK` con la lista completa de usuarios).

- [ ] **Step 3: Commit**

```bash
git add REST_API_OPTICA/inventario/API/vistas.py
git commit -m "fix: restrict UserViewSet to admin/manager roles (was privilege escalation)"
```

### Task 5: Fix bug real — typo en `ProductoProveedor.__str__`

**Problema real:** `models.py:128` usa `self.porducto_productoProveedor` (typo) pero el campo se llama `producto_productoProveedor` (línea 122). Cualquier código que llame `str(instancia)` — admin de Django, logs, shell — revienta con `AttributeError`.

**Files:**
- Modify: `REST_API_OPTICA/inventario/models.py:127-128`
- Test: `REST_API_OPTICA/inventario/tests.py`

**Interfaces:**
- Consumes: modelos `Producto`, `Proveedor`, `ProductoProveedor` ya definidos en el mismo archivo
- Produces: nada nuevo, corrige comportamiento existente

- [ ] **Step 1: Escribir test que reproduce el bug**

```python
# REST_API_OPTICA/inventario/tests.py
from django.test import TestCase
from inventario.models import Producto, Proveedor, ProductoProveedor, Categoria, Sucursal


class ProductoProveedorStrTest(TestCase):
    def test_str_no_revienta_y_muestra_nombres(self):
        sucursal = Sucursal.objects.create(nombre_sucursal="Matriz")
        categoria = Categoria.objects.create(nombre_categoria="Lentes")
        producto = Producto.objects.create(
            nombre_producto="Lente X",
            categoria_producto=categoria,
            sucursal_producto=sucursal,
            pvp_producto=10,
            costo_producto=5,
            cantidad_producto=1,
        )
        proveedor = Proveedor.objects.create(nombre_proveedor="Optica SA")
        relacion = ProductoProveedor.objects.create(
            producto_productoProveedor=producto,
            proveedor_productoProveedor=proveedor,
            costo_productoProveedor=5,
        )
        self.assertEqual(str(relacion), "Optica SA - Lente X")
```

- [ ] **Step 2: Correr el test, confirmar que falla con `AttributeError`**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py test inventario.tests.ProductoProveedorStrTest -v 2
```

Expected: `FAIL` — `AttributeError: 'ProductoProveedor' object has no attribute 'porducto_productoProveedor'`

- [ ] **Step 3: Arreglar el typo en models.py línea 128** — reemplazar:

```python
    def __str__(self):
        return f"{self.proveedor_productoProveedor.nombre_proveedor} - {self.porducto_productoProveedor.nombre_producto}"
```

por:

```python
    def __str__(self):
        return f"{self.proveedor_productoProveedor.nombre_proveedor} - {self.producto_productoProveedor.nombre_producto}"
```

- [ ] **Step 4: Correr el test de nuevo, confirmar que pasa**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py test inventario.tests.ProductoProveedorStrTest -v 2
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add REST_API_OPTICA/inventario/models.py REST_API_OPTICA/inventario/tests.py
git commit -m "fix: typo in ProductoProveedor.__str__ causing AttributeError"
```

### Task 6: Quitar `print()` de debug en `LogoutView`

**Files:**
- Modify: `REST_API_OPTICA/inventario/API/vistas.py:75-89`

- [ ] **Step 1: Editar vistas.py línea 77** — eliminar:

```python
        print("Cuerpo recibido:", request.data)  # Esto imprimirá el cuerpo enviado desde Postman
```

- [ ] **Step 2: Commit**

```bash
git add REST_API_OPTICA/inventario/API/vistas.py
git commit -m "chore: remove debug print from LogoutView"
```

---

## Fase 2 — Convenciones Django (nombres, imports, DRY)

### Task 7: Renombrar archivos a convención estándar Django

**Por qué:** cualquier dev Django que abra el repo espera `views.py`, `urls.py`, `serializers.py`. Nombres en español (`vistas.py`, `rutas.py`, `serializador.py`) son friction innecesaria para un ejemplo de portafolio.

**Files:**
- Rename: `REST_API_OPTICA/inventario/API/vistas.py` → `views.py`
- Rename: `REST_API_OPTICA/inventario/API/rutas.py` → `urls.py`
- Rename: `REST_API_OPTICA/inventario/API/serializador.py` → `serializers.py`
- Modify: `REST_API_OPTICA/REST_API_OPTICA/urls.py:3,8`

**Interfaces:**
- Consumes: nada nuevo, mismos nombres de clases (`categoriaViewSet`, `UserSerializer`, etc.) — no se renombran clases en este task
- Produces: mismos módulos con paths nuevos, usados por `REST_API_OPTICA/urls.py`

- [ ] **Step 1: Renombrar con git mv (preserva historial)**

```bash
git mv REST_API_OPTICA/inventario/API/vistas.py REST_API_OPTICA/inventario/API/views.py
git mv REST_API_OPTICA/inventario/API/rutas.py REST_API_OPTICA/inventario/API/urls.py
git mv REST_API_OPTICA/inventario/API/serializador.py REST_API_OPTICA/inventario/API/serializers.py
```

- [ ] **Step 2: Actualizar imports internos — dentro del nuevo `views.py`, línea 3**

```python
from inventario.API.serializador import categoriaSerializer, ProductoSerializer, proveedorSerializer, ProductoProveedorSerializer, clienteSerializer, VentaSerializer, ArticuloVentaSerializer, MovimientoInventarioSerializer, LoteSerializer, UserSerializer, UserSerializer, SucursalSerializer
```

por (también quita el `UserSerializer` duplicado):

```python
from inventario.API.serializers import categoriaSerializer, ProductoSerializer, proveedorSerializer, ProductoProveedorSerializer, clienteSerializer, VentaSerializer, ArticuloVentaSerializer, MovimientoInventarioSerializer, LoteSerializer, UserSerializer, SucursalSerializer
```

y línea 99 del mismo archivo:

```python
from inventario.API.serializador import ProductoSerializer
```

por:

```python
from inventario.API.serializers import ProductoSerializer
```

- [ ] **Step 3: Actualizar el nuevo `urls.py` (antes rutas.py) línea 2**

```python
from inventario.API.vistas import categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet, clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet, loteViewSet, UserViewSet, SucursalViewSet
```

por:

```python
from inventario.API.views import categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet, clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet, loteViewSet, UserViewSet, SucursalViewSet
```

- [ ] **Step 4: Actualizar `REST_API_OPTICA/REST_API_OPTICA/urls.py`** — reemplazar todo el archivo:

```python
from django.contrib import admin
from django.urls import path, include
from inventario.API.views import BuscarProductoView

urlpatterns = [
    path('api/', include('inventario.API.JWT.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('inventario.API.urls')),
    path('api/buscar/', BuscarProductoView.as_view(), name='buscar-producto')
]
```

- [ ] **Step 5: Verificar que el proyecto arranca y las rutas responden**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py check
venv/Scripts/python.exe REST_API_OPTICA/manage.py test inventario -v 2
```

Expected: `System check identified no issues` y tests previos (`ProductoProveedorStrTest`) siguen en `OK`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: rename API files to Django convention (views/urls/serializers)"
```

### Task 8: Limpiar imports duplicados/muertos en `views.py` y `serializers.py`

**Problema real:** `views.py` líneas 4 y 15-16 importan `User` dos veces (una de `django.contrib.auth.models`, luego la pisan con `get_user_model()`) — confuso, el primer import es dead code. Mismo patrón en `serializers.py` líneas 2 y 88-89, y `rest_framework.serializers` se importa dos veces (línea 1 y línea 88).

**Files:**
- Modify: `REST_API_OPTICA/inventario/API/views.py:1-16`
- Modify: `REST_API_OPTICA/inventario/API/serializers.py:1-6, 86-90`

- [ ] **Step 1: Editar `views.py` líneas 1-16** — reemplazar:

```python
from rest_framework import viewsets
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, User, Sucursal
from inventario.API.serializers import categoriaSerializer, ProductoSerializer, proveedorSerializer, ProductoProveedorSerializer, clienteSerializer, VentaSerializer, ArticuloVentaSerializer, MovimientoInventarioSerializer, LoteSerializer, UserSerializer, SucursalSerializer
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

#----------------------- Permisos ------------------
from rest_framework.permissions import IsAuthenticated
from inventario.API.permissions import IsAdministrador, IsGerente, IsUsuario, IsAdminOrManager
from django.contrib.auth import get_user_model
User = get_user_model()
```

por:

```python
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Sucursal
from inventario.API.serializers import categoriaSerializer, ProductoSerializer, proveedorSerializer, ProductoProveedorSerializer, clienteSerializer, VentaSerializer, ArticuloVentaSerializer, MovimientoInventarioSerializer, LoteSerializer, UserSerializer, SucursalSerializer
from inventario.API.permissions import IsAdminOrManager

User = get_user_model()
```

(Nota: `IsAdministrador`, `IsGerente`, `IsUsuario`, `AllowAny` no se usan en ningún lado de este archivo — se quitan. Si en Task 4 se usan `IsAuthenticated`/`IsAdminOrManager`, ya están importados arriba.)

- [ ] **Step 2: Editar `serializers.py` líneas 1-6** — reemplazar:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Sucursal
from django.contrib.auth import get_user_model

User = get_user_model()
```

por:

```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Sucursal

User = get_user_model()
```

- [ ] **Step 3: Editar `serializers.py` líneas 86-90** — eliminar (queda redundante con el import de arriba):

```python
#! Manejo del login

from rest_framework import serializers
from inventario.models import User, Sucursal

class UserSerializer(serializers.ModelSerializer):
```

por:

```python
class UserSerializer(serializers.ModelSerializer):
```

- [ ] **Step 4: Correr tests y check**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py check
venv/Scripts/python.exe REST_API_OPTICA/manage.py test inventario -v 2
```

Expected: sin errores de import, tests en `OK`.

- [ ] **Step 5: Commit**

```bash
git add REST_API_OPTICA/inventario/API/views.py REST_API_OPTICA/inventario/API/serializers.py
git commit -m "refactor: remove duplicate/dead imports in views and serializers"
```

### Task 9: DRY — reusar `ROL_USUARIO_CHOICES` en el modelo `User`

**Problema real:** `models.py` define `ROL_USUARIO_CHOICES` (líneas 8-12) pero `User.rol` (líneas 43-47) redefine la misma lista inline en vez de referenciarla. Cambiar un rol requiere editar dos lugares.

**Files:**
- Modify: `REST_API_OPTICA/inventario/models.py:42-47`

- [ ] **Step 1: Editar models.py líneas 42-47** — reemplazar:

```python
class User(AbstractUser):
    rol = models.CharField(max_length=20, choices=[
        ('Administrador', 'Administrador de sistemas'),
        ('Gerente', 'Gerente'),
        ('Usuario', 'Usuario normal'),
    ], default='Usuario')
```

por:

```python
class User(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROL_USUARIO_CHOICES, default='Usuario')
```

- [ ] **Step 2: Verificar que no rompe migraciones (choices no afecta el schema de DB)**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py makemigrations --check --dry-run
```

Expected: `No changes detected` (choices no genera migración).

- [ ] **Step 3: Commit**

```bash
git add REST_API_OPTICA/inventario/models.py
git commit -m "refactor: DRY User.rol choices from ROL_USUARIO_CHOICES constant"
```

### Task 10: Limpiar `urls.py` (antes rutas.py) — asignación redundante

**Files:**
- Modify: `REST_API_OPTICA/inventario/API/urls.py`

- [ ] **Step 1: Reemplazar todo el archivo** (la reasignación de `urlpatterns = router.urls` tras cada `register` es redundante, basta al final):

```python
from rest_framework.routers import DefaultRouter
from inventario.API.views import (
    categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet,
    clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet,
    loteViewSet, UserViewSet, SucursalViewSet,
)

router = DefaultRouter()
router.register('categorias', categoriaViewSet, basename='categoria')
router.register('productos', productoViewSet, basename='producto')
router.register('proveedores', proveedorViewSet, basename='proveedor')
router.register('productoproveedor', productoProveedorViewSet, basename='productoproveedor')
router.register('clientes', clienteViewSet, basename='cliente')
router.register('ventas', ventaViewSet, basename='venta')
router.register('articuloventa', articuloVentaViewSet, basename='articuloventa')
router.register('movimientos', movimientoInventarioViewSet, basename='movimiento')
router.register('lotes', loteViewSet, basename='lote')
router.register('user', UserViewSet, basename='users')
router.register('sucursales', SucursalViewSet, basename='sucursal')

urlpatterns = router.urls
```

- [ ] **Step 2: Verificar rutas intactas**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py show_urls 2>/dev/null || venv/Scripts/python.exe REST_API_OPTICA/manage.py check
```

- [ ] **Step 3: Commit**

```bash
git add REST_API_OPTICA/inventario/API/urls.py
git commit -m "refactor: deduplicate urlpatterns assignment in router config"
```

---

## Fase 3 — Calidad demostrable (tests, docs, settings por entorno)

### Task 11: Instalar `pytest-django` y cubrir permisos con tests

**Files:**
- Create: `REST_API_OPTICA/pytest.ini`
- Modify: `REST_API_OPTICA/inventario/tests.py`

**Interfaces:**
- Consumes: `IsAdminOrManager` (`inventario/API/permissions.py`), `UserViewSet` (Task 4)

- [ ] **Step 1: Instalar dependencias**

```bash
venv/Scripts/pip.exe install pytest-django pytest
venv/Scripts/pip.exe freeze > REST_API_OPTICA/requirements.txt
```

- [ ] **Step 2: Crear `REST_API_OPTICA/pytest.ini`**

```ini
[pytest]
DJANGO_SETTINGS_MODULE = REST_API_OPTICA.settings
python_files = tests.py test_*.py *_tests.py
```

- [ ] **Step 3: Agregar test de permisos al final de `tests.py`**

```python
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSetPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario_normal = User.objects.create_user(
            username="normal", password="testpass123", rol="Usuario"
        )
        self.admin = User.objects.create_user(
            username="admin", password="testpass123", rol="Administrador"
        )

    def test_usuario_normal_no_puede_listar_usuarios(self):
        self.client.force_authenticate(user=self.usuario_normal)
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_si_puede_listar_usuarios(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

- [ ] **Step 4: Correr y confirmar ambos pasan**

```bash
venv/Scripts/python.exe -m pytest REST_API_OPTICA/inventario/tests.py -v
```

Expected: 4 tests `PASSED` (los 2 de este task + `ProductoProveedorStrTest` + su setUp).

- [ ] **Step 5: Commit**

```bash
git add REST_API_OPTICA/pytest.ini REST_API_OPTICA/inventario/tests.py REST_API_OPTICA/requirements.txt
git commit -m "test: add pytest-django and permission regression tests for UserViewSet"
```

### Task 12: Settings por entorno (`base.py` / `dev.py` / `prod.py`)

**Files:**
- Create: `REST_API_OPTICA/REST_API_OPTICA/settings/__init__.py`
- Create: `REST_API_OPTICA/REST_API_OPTICA/settings/base.py`
- Create: `REST_API_OPTICA/REST_API_OPTICA/settings/dev.py`
- Create: `REST_API_OPTICA/REST_API_OPTICA/settings/prod.py`
- Delete: `REST_API_OPTICA/REST_API_OPTICA/settings.py`
- Modify: `REST_API_OPTICA/manage.py`
- Modify: `REST_API_OPTICA/REST_API_OPTICA/wsgi.py`
- Modify: `REST_API_OPTICA/REST_API_OPTICA/asgi.py`

**Interfaces:**
- Consumes: contenido actual de `settings.py` (post Task 3, ya con `django-environ`)
- Produces: `DJANGO_SETTINGS_MODULE=REST_API_OPTICA.settings.dev` (default local) / `.prod` (producción)

- [ ] **Step 1: Crear carpeta y mover contenido base**

```bash
mkdir REST_API_OPTICA/REST_API_OPTICA/settings
git mv REST_API_OPTICA/REST_API_OPTICA/settings.py REST_API_OPTICA/REST_API_OPTICA/settings/base.py
```

- [ ] **Step 2: En `base.py`, quitar `DEBUG`, `ALLOWED_HOSTS`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` (se definen por entorno) — reemplazar el bloque de Task 3 Step 4** por:

```python
from pathlib import Path
from datetime import timedelta
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

SECRET_KEY = env('SECRET_KEY')
```

(`BASE_DIR` sube un nivel más porque `base.py` ahora vive en `settings/`.)

- [ ] **Step 3: Crear `REST_API_OPTICA/REST_API_OPTICA/settings/dev.py`**

```python
from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CORS_ALLOW_ALL_ORIGINS = True
```

- [ ] **Step 4: Crear `REST_API_OPTICA/REST_API_OPTICA/settings/prod.py`**

```python
from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')  # obligatorio en prod, sin default
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
```

- [ ] **Step 5: Crear `REST_API_OPTICA/REST_API_OPTICA/settings/__init__.py`** (vacío, solo pa' que sea paquete)

```python
```

- [ ] **Step 6: Actualizar `manage.py`** — buscar la línea:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REST_API_OPTICA.settings')
```

por:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REST_API_OPTICA.settings.dev')
```

- [ ] **Step 7: Actualizar `wsgi.py` y `asgi.py`** — misma línea, mismo cambio (`REST_API_OPTICA.settings` → `REST_API_OPTICA.settings.dev`). Para el deploy real de producción, se sobreescribe con la variable de entorno `DJANGO_SETTINGS_MODULE=REST_API_OPTICA.settings.prod` en el servidor, sin tocar el archivo.

- [ ] **Step 8: Verificar**

```bash
venv/Scripts/python.exe REST_API_OPTICA/manage.py check
venv/Scripts/python.exe -m pytest REST_API_OPTICA/inventario/tests.py -v
```

Expected: sin errores, todos los tests en `PASSED`.

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "refactor: split settings into base/dev/prod modules"
```

### Task 13: README con arquitectura y decisiones (documenta el "por qué" pa' el portafolio)

**Files:**
- Create: `README.md` (raíz del repo)

- [ ] **Step 1: Escribir README con: descripción del proyecto, stack, cómo correrlo local (`.env.example` → `.env`, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver`), estructura de carpetas explicada, decisiones de arquitectura (por qué 1 app, por qué settings split, roles y permisos).**

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with setup instructions and architecture notes"
```

---

## Self-Review

- **Cobertura:** Fase 0 (repo limpio) → Fase 1 (seguridad: secrets, permisos, bug crítico) → Fase 2 (convenciones Django) → Fase 3 (tests + settings + docs). Cubre todo lo detectado en la inspección real del código (models.py, views.py/vistas.py, urls.py/rutas.py, serializers.py/serializador.py, permissions.py, settings.py).
- **Placeholders:** ninguno — cada step tiene código completo y comando exacto.
- **Consistencia de nombres:** `views.py`/`urls.py`/`serializers.py` usados consistentemente desde Task 7 en adelante; Task 8-10 asumen los nombres ya renombrados.
- **No incluido a propósito (YAGNI):** split en múltiples apps (`accounts`/`inventory`/`sales`) — el dominio es cohesivo, dividir ahora es prematuro sin necesidad real de escalar equipos/despliegues independientes. Si se quiere de todos modos como demostración de DDD, es un plan aparte (migraciones cruzadas de FK son delicadas).

---

**Plan completo, guardado en `docs/superpowers/plans/2026-07-12-django-best-practices-refactor.md`.**

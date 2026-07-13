from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from inventario.models import Producto, Proveedor, ProductoProveedor, Categoria, Sucursal

User = get_user_model()


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
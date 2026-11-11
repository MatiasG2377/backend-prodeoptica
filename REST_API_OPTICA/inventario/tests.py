from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from inventario.models import Producto, Proveedor, ProductoProveedor, Categoria, Sucursal, Cliente, Venta, Abono, Paciente, FichaMedica, MovimientoInventario

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


class AbonoCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)
        self.cliente = Cliente.objects.create(nombre_cliente="Juan", apellido_cliente="Perez")
        self.sucursal = Sucursal.objects.create(nombre_sucursal="Central")
        self.venta = Venta.objects.create(
            cliente_venta=self.cliente,
            sucursal_venta=self.sucursal,
            total_venta=50.00,
            estado_venta="P",
        )

    def test_crear_abono_con_venta_id(self):
        response = self.client.post("/api/abonos/", {
            "venta_id": self.venta.id,
            "cliente_id": self.cliente.id,
            "monto": "15.00",
            "metodo_pago": "Efectivo",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Abono.objects.filter(venta=self.venta).count(), 1)

    def test_crear_abono_con_venta_en_lugar_de_venta_id(self):
        response = self.client.post("/api/abonos/", {
            "venta": self.venta.id,
            "cliente": self.cliente.id,
            "monto": "10.00",
            "metodo_pago": "Efectivo",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Abono.objects.filter(venta=self.venta).count(), 1)


class FichaMedicaCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="optometra", password="password123")
        self.client.force_authenticate(user=self.user)
        self.sucursal = Sucursal.objects.create(nombre_sucursal="Matriz - Centro Histórico")
        self.paciente = Paciente.objects.create(nombres_paciente="Ana", apellidos_paciente="Lopez")

    def test_crear_ficha_con_sucursal_str(self):
        response = self.client.post("/api/fichas-medicas/", {
            "paciente": self.paciente.id,
            "usuario": self.user.id,
            "sucursal": "Matriz - Centro Histórico",
            "altura": 25,
            "material": "gx7",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FichaMedica.objects.count(), 1)

    def test_crear_ficha_con_sucursal_id(self):
        response = self.client.post("/api/fichas-medicas/", {
            "paciente": self.paciente.id,
            "usuario": self.user.id,
            "sucursal": self.sucursal.id,
            "altura": 25,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MovimientoInventarioCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="inventario_user", password="password123")
        self.client.force_authenticate(user=self.user)
        self.sucursal = Sucursal.objects.create(nombre_sucursal="Matriz")
        self.categoria = Categoria.objects.create(nombre_categoria="Armazones")
        self.producto = Producto.objects.create(
            nombre_producto="CH 345",
            categoria_producto=self.categoria,
            sucursal_producto=self.sucursal,
            pvp_producto=23.00,
            costo_producto=10.00,
            cantidad_producto=2,
        )

    def test_crear_movimiento_con_kardex_payload(self):
        # El frontend envía campos con sufijo _kardex a /api/kardex/
        response = self.client.post("/api/kardex/", {
            "producto_kardex": self.producto.id,
            "tipo_kardex": "Entrada",
            "cantidad_kardex": 2,
            "referencia_kardex": "FACTURA N°202020852",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MovimientoInventario.objects.filter(producto_movimientoInventario=self.producto).count(), 1)

    def test_historial_kardex_expone_alias_kardex(self):
        MovimientoInventario.objects.create(
            producto_movimientoInventario=self.producto,
            sucursal_movimientoInventario=self.sucursal,
            tipo_movimientoInventario="Entrada",
            cantidad_movimientoInventario=2,
            motivo_movimientoInventario="Factura 1",
        )
        response = self.client.get(f"/api/kardex/historial/{self.producto.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        item = response.data[0]
        self.assertIn("tipo_kardex", item)
        self.assertEqual(item["tipo_kardex"], "Entrada")
        self.assertIn("cantidad_kardex", item)
        self.assertEqual(item["cantidad_kardex"], 2)



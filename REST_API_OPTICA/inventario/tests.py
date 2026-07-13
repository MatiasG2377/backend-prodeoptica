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
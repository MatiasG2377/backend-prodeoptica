from rest_framework import serializers

from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, MovimientoInventario, Lote


class categoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class proveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


# Serializador para el producto
class ProductoSerializer(serializers.ModelSerializer):
    # Incluyendo nombre de la categoría y sucursal en la representación
    categoria_nombre = serializers.CharField(source='categoria_producto.nombre_categoria', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_producto.nombre_sucursal', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'


# Serializador para la relación entre productos y proveedores
class ProductoProveedorSerializer(serializers.ModelSerializer):
    # Relación anidada para representación
    producto_nombre = serializers.CharField(source='producto_productoProveedor.nombre_producto', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor_productoProveedor.nombre_proveedor', read_only=True)

    class Meta:
        model = ProductoProveedor
        fields = '__all__'


# Serializador para movimientos de inventario
class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto_movimientoInventario.nombre_producto', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_movimientoInventario.nombre_sucursal', read_only=True)

    class Meta:
        model = MovimientoInventario
        fields = '__all__'


# Serializador para lotes de productos
class LoteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto_lote.nombre_producto', read_only=True)

    class Meta:
        model = Lote
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth import get_user_model
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, Sucursal

User = get_user_model()

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

class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

# Serializador para la venta
class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente_venta.nombre_cliente', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_venta.nombre_sucursal', read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'

# Serializador para los artículos vendidos en una venta
class ArticuloVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto_articuloVenta.nombre_producto', read_only=True)
    venta_fecha = serializers.DateTimeField(source='venta_articuloVenta.fecha_venta', read_only=True)

    class Meta:
        model = ArticuloVenta
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



# Serializador para la sucursal
class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

#! Manejo del login

class UserSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre de la sucursal
    sucursal_nombre = serializers.CharField(source='sucursal_usuario.nombre_sucursal', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'rol', 'sucursal_usuario', 'sucursal_nombre']
        extra_kwargs = {'password': {'write_only': True}}  # La contraseña solo se envía, no se devuelve en la respuesta

    def create(self, validated_data):
        # Crear un usuario con contraseña encriptada
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'Usuario'),  # Valor predeterminado para el rol
            sucursal_usuario=validated_data.get('sucursal_usuario')  # Asignar la sucursal
        )
        return user

    def update(self, instance, validated_data):
        # Extraer la contraseña si está presente
        password = validated_data.pop('password', None)
        # Actualizar los demás campos
        user = super().update(instance, validated_data)
        # Asignar y hashear la contraseña si se proporciona
        if password:
            user.set_password(password)
            user.save()
        return user

from rest_framework import serializers

from inventario.models import Cliente, Venta, ArticuloVenta


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

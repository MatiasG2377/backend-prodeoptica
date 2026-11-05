from rest_framework import serializers

from inventario.models import (
    Laboratorio,
    Cliente,
    Paciente,
    FichaMedica,
    Venta,
    ArticuloVenta,
    Abono,
    Egreso,
)


class LaboratorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorio
        fields = '__all__'


class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    cliente_info = clienteSerializer(source='cliente', read_only=True)

    class Meta:
        model = Paciente
        fields = '__all__'


class FichaMedicaSerializer(serializers.ModelSerializer):
    paciente_info = PacienteSerializer(source='paciente', read_only=True)

    class Meta:
        model = FichaMedica
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Aplanar datos ópticos para que el frontend los lea directamente
        if instance.datos_opticos and isinstance(instance.datos_opticos, dict):
            for k, v in instance.datos_opticos.items():
                if k not in data:
                    data[k] = v
        return data

    def to_internal_value(self, data):
        # Campos estándar de FichaMedica
        standard_fields = {'id', 'paciente', 'usuario', 'sucursal', 'fecha', 'datos_opticos'}
        datos_opticos = {}
        cleaned_data = {}
        for k, v in data.items():
            if k in standard_fields:
                cleaned_data[k] = v
            else:
                datos_opticos[k] = v
        
        if 'datos_opticos' in cleaned_data and isinstance(cleaned_data['datos_opticos'], dict):
            datos_opticos.update(cleaned_data['datos_opticos'])
        cleaned_data['datos_opticos'] = datos_opticos
        return super().to_internal_value(cleaned_data)


# Serializador para la venta
class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente_venta.nombre_cliente', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_venta.nombre_sucursal', read_only=True)
    cliente = clienteSerializer(source='cliente_venta', read_only=True)

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


# Serializador para Abonos
class AbonoSerializer(serializers.ModelSerializer):
    tieneAbono = serializers.BooleanField(read_only=True, default=True)
    cliente = clienteSerializer(read_only=True)
    venta = VentaSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source='cliente', write_only=True, required=False, allow_null=True
    )
    venta_id = serializers.PrimaryKeyRelatedField(
        queryset=Venta.objects.all(), source='venta', write_only=True
    )

    class Meta:
        model = Abono
        fields = [
            'id',
            'venta',
            'venta_id',
            'cliente',
            'cliente_id',
            'monto',
            'fecha',
            'metodo_pago',
            'completado',
            'tieneAbono',
        ]

    def create(self, validated_data):
        # Si no viene cliente especificado, inferir de la venta
        if not validated_data.get('cliente') and validated_data.get('venta'):
            validated_data['cliente'] = validated_data['venta'].cliente_venta
        return super().create(validated_data)


# Serializador para Egresos
class EgresoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario_egreso.username_usuario', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_egreso.nombre_sucursal', read_only=True)

    class Meta:
        model = Egreso
        fields = '__all__'

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
    Sucursal,
    User,
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

        # Normalizar sucursal (acepta ID int, string numérico "1", objeto {"id": 1}, o nombre "Matriz")
        sucursal_val = cleaned_data.get('sucursal')
        if sucursal_val is not None and sucursal_val != '':
            if isinstance(sucursal_val, dict):
                cleaned_data['sucursal'] = sucursal_val.get('id', 1)
            elif isinstance(sucursal_val, str) and not sucursal_val.isdigit():
                suc_obj = Sucursal.objects.filter(nombre_sucursal__iexact=sucursal_val).first()
                if not suc_obj:
                    suc_obj = Sucursal.objects.filter(nombre_sucursal__icontains=sucursal_val).first()
                cleaned_data['sucursal'] = suc_obj.id if suc_obj else 1
            else:
                try:
                    cleaned_data['sucursal'] = int(sucursal_val)
                except (ValueError, TypeError):
                    cleaned_data['sucursal'] = 1
        else:
            cleaned_data['sucursal'] = 1

        # Normalizar usuario si viene como username o dict
        usuario_val = cleaned_data.get('usuario')
        if usuario_val is not None and usuario_val != '':
            if isinstance(usuario_val, dict):
                cleaned_data['usuario'] = usuario_val.get('id')
            elif isinstance(usuario_val, str) and not usuario_val.isdigit():
                u_obj = User.objects.filter(username__iexact=usuario_val).first()
                cleaned_data['usuario'] = u_obj.id if u_obj else None
            else:
                try:
                    cleaned_data['usuario'] = int(usuario_val)
                except (ValueError, TypeError):
                    cleaned_data['usuario'] = None

        return super().to_internal_value(cleaned_data)


# Serializador para la venta
class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente_venta.nombre_cliente', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_venta.nombre_sucursal', read_only=True)
    cliente = clienteSerializer(source='cliente_venta', read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)

        # Normalizar sucursal_venta
        suc = data_copy.get('sucursal_venta')
        if suc is not None and suc != '':
            if isinstance(suc, dict):
                data_copy['sucursal_venta'] = suc.get('id', 1)
            elif isinstance(suc, str) and not suc.isdigit():
                suc_obj = Sucursal.objects.filter(nombre_sucursal__iexact=suc).first() or Sucursal.objects.filter(nombre_sucursal__icontains=suc).first()
                data_copy['sucursal_venta'] = suc_obj.id if suc_obj else 1
            else:
                try:
                    data_copy['sucursal_venta'] = int(suc)
                except (ValueError, TypeError):
                    first_suc = Sucursal.objects.first()
                    data_copy['sucursal_venta'] = first_suc.id if first_suc else 1
        else:
            first_suc = Sucursal.objects.first()
            data_copy['sucursal_venta'] = first_suc.id if first_suc else 1

        # Normalizar usuario_venta
        usr = data_copy.get('usuario_venta')
        if usr is not None and usr != '':
            if isinstance(usr, dict):
                data_copy['usuario_venta'] = usr.get('id')
            elif isinstance(usr, str) and not usr.isdigit():
                u_obj = User.objects.filter(username__iexact=usr).first()
                data_copy['usuario_venta'] = u_obj.id if u_obj else None
            else:
                try:
                    data_copy['usuario_venta'] = int(usr)
                except (ValueError, TypeError):
                    data_copy['usuario_venta'] = None

        return super().to_internal_value(data_copy)


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

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'venta' in data_copy and 'venta_id' not in data_copy:
            val = data_copy['venta']
            data_copy['venta_id'] = val.get('id') if isinstance(val, dict) else val
        if 'cliente' in data_copy and 'cliente_id' not in data_copy:
            val = data_copy['cliente']
            if val == '' or val is None:
                data_copy['cliente_id'] = None
            else:
                data_copy['cliente_id'] = val.get('id') if isinstance(val, dict) else val
        return super().to_internal_value(data_copy)

    def create(self, validated_data):
        # Si no viene cliente especificado, inferir de la venta
        if not validated_data.get('cliente') and validated_data.get('venta'):
            validated_data['cliente'] = validated_data['venta'].cliente_venta
        return super().create(validated_data)


# Serializador para Egresos
class EgresoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario_egreso.username', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal_egreso.nombre_sucursal', read_only=True)

    class Meta:
        model = Egreso
        fields = '__all__'

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)

        # Normalizar sucursal_egreso
        suc = data_copy.get('sucursal_egreso')
        if suc is not None and suc != '':
            if isinstance(suc, dict):
                data_copy['sucursal_egreso'] = suc.get('id', 1)
            elif isinstance(suc, str) and not suc.isdigit():
                suc_obj = Sucursal.objects.filter(nombre_sucursal__iexact=suc).first() or Sucursal.objects.filter(nombre_sucursal__icontains=suc).first()
                data_copy['sucursal_egreso'] = suc_obj.id if suc_obj else 1
            else:
                try:
                    data_copy['sucursal_egreso'] = int(suc)
                except (ValueError, TypeError):
                    first_suc = Sucursal.objects.first()
                    data_copy['sucursal_egreso'] = first_suc.id if first_suc else 1
        else:
            first_suc = Sucursal.objects.first()
            data_copy['sucursal_egreso'] = first_suc.id if first_suc else 1

        # Normalizar usuario_egreso
        usr = data_copy.get('usuario_egreso')
        if usr is not None and usr != '':
            if isinstance(usr, dict):
                data_copy['usuario_egreso'] = usr.get('id')
            elif isinstance(usr, str) and not usr.isdigit():
                u_obj = User.objects.filter(username__iexact=usr).first()
                data_copy['usuario_egreso'] = u_obj.id if u_obj else None
            else:
                try:
                    data_copy['usuario_egreso'] = int(usr)
                except (ValueError, TypeError):
                    data_copy['usuario_egreso'] = None

        return super().to_internal_value(data_copy)

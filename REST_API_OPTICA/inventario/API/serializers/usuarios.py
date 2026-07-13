from rest_framework import serializers
from django.contrib.auth import get_user_model

from inventario.models import Sucursal
from inventario.services import crear_usuario, actualizar_usuario

User = get_user_model()


# Serializador para la sucursal
class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre de la sucursal
    sucursal_nombre = serializers.CharField(source='sucursal_usuario.nombre_sucursal', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'rol', 'sucursal_usuario', 'sucursal_nombre']
        extra_kwargs = {'password': {'write_only': True}}  # La contraseña solo se envía, no se devuelve en la respuesta

    def create(self, validated_data):
        return crear_usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            rol=validated_data.get('rol', 'Usuario'),
            sucursal_usuario=validated_data.get('sucursal_usuario'),
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        return actualizar_usuario(user=instance, password=password, **validated_data)

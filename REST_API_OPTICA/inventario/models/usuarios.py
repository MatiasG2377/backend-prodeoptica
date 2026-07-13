from django.db import models
from django.contrib.auth.models import AbstractUser

# Opciones de roles para los usuarios
ROL_USUARIO_CHOICES = [
    ('Administrador', 'Administrador de sistemas'),
    ('Gerente', 'Gerente'),
    ('Usuario', 'Usuario normal'),
]


# Tabla de sucursales
class Sucursal(models.Model):
    nombre_sucursal = models.TextField(null=False)  # Nombre de la sucursal
    direccion_sucursal = models.TextField(blank=True, null=True)  # Dirección de la sucursal
    telefono_sucursal = models.TextField(blank=True, null=True)  # Teléfono de la sucursal
    gerente_sucursal = models.TextField(blank=True, null=True)  # Nombre del gerente encargado
    fecha_creacion_sucursal = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return self.nombre_sucursal


class User(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROL_USUARIO_CHOICES, default='Usuario')
    sucursal_usuario = models.ForeignKey('Sucursal', on_delete=models.SET_NULL, null=True, blank=True)

    # Agrega related_name personalizado para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Cambia el related_name para evitar conflicto
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Cambia el related_name para evitar conflicto
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} - {self.rol}"

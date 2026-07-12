from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Opciones de roles para los usuarios
ROL_USUARIO_CHOICES = [
    ('Administrador', 'Administrador de sistemas'),
    ('Gerente', 'Gerente'),
    ('Usuario', 'Usuario normal'),
]

#! Opciones para los estados de los productos
ESTADO_PRODUCTO_CHOICES = [
    ('Disponible', 'Disponible'),
    ('Reservado', 'Reservado'),
    ('Agotado', 'Agotado'),
]

#! Opciones para los estados de las ventas
ESTADO_VENTA_CHOICES = [
    ('P', 'Pendiente'),
    ('C', 'Cancelado'),
    ('F', 'Finalizado'),
]


#! Los ID de cada tabla se generan de manera automática en la BD

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
# Categoría de productos
class Categoria(models.Model):
    nombre_categoria = models.TextField(null=False) # Nombre de la categoría
    descripcion_categoria = models.TextField(blank=True, null=True) # Descripción de la categoría
    activo_categoria = models.BooleanField(default=True) # Este campo sirve para eliminación lógica de categorías
    relevancia_categoria = models.IntegerField(default=0)  # Servirá para establecer un orden dentro de los datos 
    fecha_creacion_categoria = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    actualizacion_categoria = models.DateTimeField(auto_now=True)      # Fecha de última actualización

    def __str__(self):
        return self.nombre_categoria


# Proveedores
class Proveedor(models.Model):
    nombre_proveedor = models.TextField(null=False) # Nombre de la empresa proveedora
    informacion_proveedor = models.TextField(blank=True, null=True) # Información del proveedor
    correo_proveedor = models.EmailField(unique=True, blank=True, null=True) # Correo electrónico del proveedor
    telefono_proveedor = models.TextField(blank=True, null=True) # Número telefónico del proveedor
    direccion_proveedor = models.TextField(blank=True, null=True) # Dirección del proveedor

    def __str__(self):
        return self.nombre_proveedor


class Producto(models.Model):
    nombre_producto = models.TextField(null=False)  # Nombre del producto
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría
    sucursal_producto = models.ForeignKey(
        Sucursal, 
        on_delete=models.CASCADE,
        default=1  # ID de la sucursal predeterminada
    )  # Sucursal asociada
    pvp_producto = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # Precio de venta
    costo_producto = models.DecimalField(max_digits=10, decimal_places=2)  # Costo
    cantidad_producto = models.IntegerField(null=False)  # Cantidad disponible
    minimo_producto = models.IntegerField(default=0)  # Stock mínimo
    maximo_producto = models.IntegerField(default=100)  # Stock máximo
    estado_producto = models.CharField(max_length=20, choices=ESTADO_PRODUCTO_CHOICES, default='Disponible')  # Estado
    descripcion_producto = models.TextField(blank=True, null=True)  # Descripción
    marca_producto = models.TextField(blank=True, null=True)  # Marca
    ultima_venta_producto = models.DateTimeField(blank=True, null=True)  # Última venta
        
    def clean(self):
        if self.minimo_producto > self.maximo_producto:
            raise ValidationError("El stock mínimo no puede ser mayor que el stock máximo.")
        if self.cantidad_producto < 0:
            raise ValidationError("La cantidad en stock no puede ser negativa.")

    def __str__(self):
        return f"{self.nombre_producto}"

# Relación entre Productos y Proveedores
class ProductoProveedor(models.Model):
    producto_productoProveedor  = models.ForeignKey(Producto, on_delete=models.CASCADE) # ForeignKey del Producto
    proveedor_productoProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE) # ForeignKey del proveedor
    costo_productoProveedor = models.DecimalField(max_digits=10, decimal_places=2) # Registrar el costo de adquisición del producto
    tiempo_entrega_productoProveedor = models.IntegerField(help_text="Días para entrega", blank=True, null=True) # Registrar el tiempo en dpias de entrega

    def __str__(self):
        return f"{self.proveedor_productoProveedor.nombre_proveedor} - {self.porducto_productoProveedor.nombre_producto}"


# Clientes
class Cliente(models.Model):
    ci_cliente = models.TextField(null=False) # Identificación del cliente
    nombre_cliente = models.TextField(null=False) # Nombre del cliente
    informacion_cliente = models.TextField(blank=True, null=True) # Información del cliente
    correo_cliente = models.EmailField(unique=True, blank=True, null=True) # Correo del cliente
    telefono_cliente = models.TextField(blank=True, null=True) # Teléfono del cliente
    direccion_cliente = models.TextField(blank=True, null=True) # Dirección del cliente

    def __str__(self):
        return self.nombre_cliente


# Ventas
class Venta(models.Model):
    cliente_venta = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)  # Cliente
    sucursal_venta = models.ForeignKey(
        Sucursal, 
        on_delete=models.CASCADE, 
        default=1  # Cambia '1' por el ID de una sucursal válida en tu base de datos
    )  # Sucursal
    fecha_venta = models.DateTimeField(auto_now_add=True)  # Fecha
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total
    estado_venta = models.CharField(max_length=1, choices=ESTADO_VENTA_CHOICES, default='P')  # Estado

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_venta}"


# Artículos vendidos en una venta
class ArticuloVenta(models.Model):
    venta_articuloVenta = models.ForeignKey(Venta, on_delete=models.CASCADE) # ForeignKey de la venta
    producto_articuloVenta = models.ForeignKey(Producto, on_delete=models.CASCADE) # ForeignKey del producto
    cantidad_articuloVenta = models.IntegerField(null=False) #Cnatidad de producto en la venta
    pvp_articuloVenta = models.DecimalField(max_digits=10, decimal_places=2, null=False) # Precio 
    descuento_articuloVenta = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) # Descuento del producto

    def __str__(self):
        return f"Artículo {self.producto_articuloVenta.nombre_producto} en Venta #{self.venta_articuloVenta.id}"


class MovimientoInventario(models.Model):
    producto_movimientoInventario = models.ForeignKey(Producto, on_delete=models.CASCADE)  # ForeignKey del producto
    sucursal_movimientoInventario = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        default=1  # ID de la sucursal predeterminada
    )
    tipo_movimientoInventario = models.CharField(
        max_length=10,
        choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')]
    )  # Tipo de movimiento en el inventario
    cantidad_movimientoInventario = models.IntegerField(null=False)  # Cantidad de productos movidos
    fecha_movimientoInventario = models.DateTimeField(auto_now_add=True)  # Fecha del movimiento del inventario
    motivo_movimientoInventario = models.TextField(blank=True, null=True)  # Ej: Venta, ajuste, devolución

    def __str__(self):
        return f"{self.tipo_movimientoInventario} - {self.producto_movimientoInventario.nombre_producto} ({self.cantidad_movimientoInventario})"


# Lotes de productos
class Lote(models.Model):
    producto_lote = models.ForeignKey(Producto, on_delete=models.CASCADE) # ForeignKey del producto
    cantidad_lote = models.IntegerField() # Cantidad de unidades en el lote
    fecha_ingreso_lote = models.DateTimeField(auto_now_add=True) # Fecha de ingreso en el lote
    fecha_caducidad_lote = models.DateField(blank=True, null=True) # Fecha de caducidad en productos que aplique

    def __str__(self):
        return f"Lote de {self.producto_lote.nombre_producto} ({self.cantidad_lote} unidades)"

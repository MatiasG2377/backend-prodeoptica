from django.db import models

from .usuarios import Sucursal
from .inventario import Producto

#! Opciones para los estados de las ventas
ESTADO_VENTA_CHOICES = [
    ('P', 'Pendiente'),
    ('C', 'Cancelado'),
    ('F', 'Finalizado'),
]


# Clientes
class Cliente(models.Model):
    ci_cliente = models.TextField(null=False)  # Identificación del cliente
    nombre_cliente = models.TextField(null=False)  # Nombre del cliente
    informacion_cliente = models.TextField(blank=True, null=True)  # Información del cliente
    correo_cliente = models.EmailField(unique=True, blank=True, null=True)  # Correo del cliente
    telefono_cliente = models.TextField(blank=True, null=True)  # Teléfono del cliente
    direccion_cliente = models.TextField(blank=True, null=True)  # Dirección del cliente

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
    venta_articuloVenta = models.ForeignKey(Venta, on_delete=models.CASCADE)  # ForeignKey de la venta
    producto_articuloVenta = models.ForeignKey(Producto, on_delete=models.CASCADE)  # ForeignKey del producto
    cantidad_articuloVenta = models.IntegerField(null=False)  # Cantidad de producto en la venta
    pvp_articuloVenta = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # Precio
    descuento_articuloVenta = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Descuento del producto

    def __str__(self):
        return f"Artículo {self.producto_articuloVenta.nombre_producto} en Venta #{self.venta_articuloVenta.id}"

from django.db import models

from .usuarios import Sucursal, User
from .inventario import Producto

#! Opciones para los estados de las ventas
ESTADO_VENTA_CHOICES = [
    ('P', 'Pendiente'),
    ('C', 'Cancelado'),
    ('F', 'Finalizado'),
]


# Laboratorios externos de óptica
class Laboratorio(models.Model):
    nombre_laboratorio = models.TextField(null=False)
    direccion_laboratorio = models.TextField(blank=True, null=True)
    telefono_laboratorio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_laboratorio


# Clientes
class Cliente(models.Model):
    ci_cliente = models.TextField(blank=True, null=True)  # Identificación del cliente (opcional)
    nombre_cliente = models.TextField(null=False)  # Nombre del cliente
    apellido_cliente = models.TextField(blank=True, null=True)  # Apellido del cliente
    informacion_cliente = models.TextField(blank=True, null=True)  # Información del cliente
    correo_cliente = models.EmailField(unique=True, blank=True, null=True)  # Correo del cliente
    telefono_cliente = models.TextField(blank=True, null=True)  # Teléfono del cliente
    direccion_cliente = models.TextField(blank=True, null=True)  # Dirección del cliente

    def __str__(self):
        if self.apellido_cliente:
            return f"{self.nombre_cliente} {self.apellido_cliente}"
        return self.nombre_cliente


# Pacientes
class Paciente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pacientes', null=True, blank=True)
    ci_paciente = models.TextField(blank=True, null=True)  # Opcional
    nombres_paciente = models.TextField(null=False)
    apellidos_paciente = models.TextField(null=False)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    ocupacion_paciente = models.TextField(blank=True, null=True)
    direccion_paciente = models.TextField(blank=True, null=True)
    telefono_paciente = models.TextField(blank=True, null=True)
    antecedentes_paciente = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombres_paciente} {self.apellidos_paciente} ({self.ci_paciente})"


# Fichas Médicas Optométricas
class FichaMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='fichas')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)
    fecha = models.DateTimeField(auto_now_add=True)
    datos_opticos = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Ficha #{self.id} - {self.paciente}"


# Ventas
class Venta(models.Model):
    cliente_venta = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)  # Cliente
    sucursal_venta = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        default=1  # ID de sucursal
    )  # Sucursal
    usuario_venta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    laboratorio_venta = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    orden_laboratorio = models.TextField(blank=True, null=True)
    orden_trabajo = models.TextField(blank=True, null=True)
    metodo_venta = models.CharField(max_length=50, default='Efectivo')
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


# Abonos / Pagos parciales
class Abono(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='abonos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, related_name='abonos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, default='Efectivo')
    completado = models.BooleanField(default=False)

    @property
    def tieneAbono(self):
        return True

    def __str__(self):
        return f"Abono #{self.id} Venta #{self.venta_id} - ${self.monto}"


# Egresos / Gastos operativos de caja
class Egreso(models.Model):
    monto_egreso = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion_egreso = models.TextField()
    categoria_egreso = models.CharField(max_length=100, default='Otros')
    metodo_pago_egreso = models.CharField(max_length=50, default='Efectivo')
    fecha_egreso = models.DateTimeField(auto_now_add=True)
    usuario_egreso = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    sucursal_egreso = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Egreso #{self.id} - ${self.monto_egreso} ({self.categoria_egreso})"

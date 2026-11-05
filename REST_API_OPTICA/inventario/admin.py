from django.contrib import admin
from .models import (
    Sucursal,
    User,
    Categoria,
    Proveedor,
    Producto,
    ProductoProveedor,
    MovimientoInventario,
    Lote,
    Laboratorio,
    Cliente,
    Paciente,
    FichaMedica,
    Venta,
    ArticuloVenta,
    Abono,
    Egreso,
)


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_sucursal', 'telefono_sucursal', 'gerente_sucursal', 'fecha_creacion_sucursal')
    search_fields = ('nombre_sucursal', 'gerente_sucursal', 'direccion_sucursal')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'rol', 'sucursal_usuario', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('rol', 'is_staff', 'is_active', 'sucursal_usuario')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_categoria', 'relevancia_categoria', 'activo_categoria')
    search_fields = ('nombre_categoria',)
    list_filter = ('activo_categoria',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_proveedor', 'correo_proveedor', 'telefono_proveedor', 'direccion_proveedor')
    search_fields = ('nombre_proveedor', 'correo_proveedor')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_producto', 'categoria_producto', 'marca_producto', 'pvp_producto', 'costo_producto', 'cantidad_producto', 'estado_producto', 'sucursal_producto')
    search_fields = ('nombre_producto', 'marca_producto')
    list_filter = ('categoria_producto', 'estado_producto', 'sucursal_producto')


@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto_productoProveedor', 'proveedor_productoProveedor', 'costo_productoProveedor', 'tiempo_entrega_productoProveedor')
    search_fields = ('producto_productoProveedor__nombre_producto', 'proveedor_productoProveedor__nombre_proveedor')


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto_movimientoInventario', 'sucursal_movimientoInventario', 'tipo_movimientoInventario', 'cantidad_movimientoInventario', 'fecha_movimientoInventario', 'motivo_movimientoInventario')
    list_filter = ('tipo_movimientoInventario', 'sucursal_movimientoInventario')
    search_fields = ('producto_movimientoInventario__nombre_producto', 'motivo_movimientoInventario')


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto_lote', 'cantidad_lote', 'fecha_ingreso_lote', 'fecha_caducidad_lote')
    search_fields = ('producto_lote__nombre_producto',)


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_laboratorio', 'telefono_laboratorio', 'direccion_laboratorio')
    search_fields = ('nombre_laboratorio',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'ci_cliente', 'nombre_cliente', 'apellido_cliente', 'correo_cliente', 'telefono_cliente')
    search_fields = ('ci_cliente', 'nombre_cliente', 'apellido_cliente', 'correo_cliente')


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'ci_paciente', 'nombres_paciente', 'apellidos_paciente', 'fecha_nacimiento', 'telefono_paciente', 'cliente')
    search_fields = ('ci_paciente', 'nombres_paciente', 'apellidos_paciente')


@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'usuario', 'sucursal', 'fecha')
    list_filter = ('sucursal', 'fecha')
    search_fields = ('paciente__nombres_paciente', 'paciente__apellidos_paciente', 'paciente__ci_paciente')


class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    extra = 1


class AbonoInline(admin.TabularInline):
    model = Abono
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_venta', 'sucursal_venta', 'total_venta', 'metodo_venta', 'estado_venta', 'fecha_venta')
    list_filter = ('estado_venta', 'metodo_venta', 'sucursal_venta')
    search_fields = ('cliente_venta__nombre_cliente', 'cliente_venta__ci_cliente')
    inlines = [ArticuloVentaInline, AbonoInline]


@admin.register(ArticuloVenta)
class ArticuloVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta_articuloVenta', 'producto_articuloVenta', 'cantidad_articuloVenta', 'pvp_articuloVenta', 'descuento_articuloVenta')
    search_fields = ('producto_articuloVenta__nombre_producto',)


@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'cliente', 'monto', 'metodo_pago', 'completado', 'fecha')
    list_filter = ('completado', 'metodo_pago')
    search_fields = ('venta__id', 'cliente__nombre_cliente')


@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'monto_egreso', 'categoria_egreso', 'metodo_pago_egreso', 'sucursal_egreso', 'fecha_egreso', 'descripcion_egreso')
    list_filter = ('categoria_egreso', 'metodo_pago_egreso', 'sucursal_egreso')
    search_fields = ('descripcion_egreso',)

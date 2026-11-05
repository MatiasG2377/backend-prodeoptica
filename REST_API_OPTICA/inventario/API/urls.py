from django.urls import path
from rest_framework.routers import DefaultRouter
from inventario.API.views import (
    categoriaViewSet,
    productoViewSet,
    proveedorViewSet,
    productoProveedorViewSet,
    clienteViewSet,
    PacienteViewSet,
    FichaMedicaViewSet,
    ventaViewSet,
    articuloVentaViewSet,
    movimientoInventarioViewSet,
    loteViewSet,
    LaboratorioViewSet,
    AbonoViewSet,
    EgresoViewSet,
    CierreCajaResumenView,
    UserViewSet,
    SucursalViewSet,
)

router = DefaultRouter()
router.register('categorias', categoriaViewSet, basename='categoria')
router.register('productos', productoViewSet, basename='producto')
router.register('proveedores', proveedorViewSet, basename='proveedor')
router.register('productoproveedor', productoProveedorViewSet, basename='productoproveedor')
router.register('laboratorios', LaboratorioViewSet, basename='laboratorio')
router.register('clientes', clienteViewSet, basename='cliente')
router.register('cliente-paciente', clienteViewSet, basename='cliente-paciente')
router.register('pacientes', PacienteViewSet, basename='paciente')
router.register('fichas-medicas', FichaMedicaViewSet, basename='ficha-medica')
router.register('ventas', ventaViewSet, basename='venta')
router.register('articuloventa', articuloVentaViewSet, basename='articuloventa')
router.register('articulos-venta', articuloVentaViewSet, basename='articulos-venta')
router.register('abonos', AbonoViewSet, basename='abono')
router.register('egresos', EgresoViewSet, basename='egreso')
router.register('movimientos', movimientoInventarioViewSet, basename='movimiento')
router.register('movimientos-inventario', movimientoInventarioViewSet, basename='movimientos-inventario')
router.register('lotes', loteViewSet, basename='lote')
router.register('kardex', movimientoInventarioViewSet, basename='kardex')
router.register('user', UserViewSet, basename='users')
router.register('usuarios', UserViewSet, basename='usuarios')
router.register('sucursales', SucursalViewSet, basename='sucursal')

urlpatterns = [
    path('dashboard/cierre-caja-resumen/', CierreCajaResumenView.as_view(), name='cierre-caja-resumen'),
] + router.urls

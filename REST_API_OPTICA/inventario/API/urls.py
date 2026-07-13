from rest_framework.routers import DefaultRouter
from inventario.API.views import categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet, clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet, loteViewSet, UserViewSet, SucursalViewSet

router = DefaultRouter()
router.register('categorias', categoriaViewSet, basename='categoria')
router.register('productos', productoViewSet, basename='producto')
router.register('proveedores', proveedorViewSet, basename='proveedor')
router.register('productoproveedor', productoProveedorViewSet, basename='productoproveedor')
router.register('clientes', clienteViewSet, basename='cliente')
router.register('ventas', ventaViewSet, basename='venta')
router.register('articuloventa', articuloVentaViewSet, basename='articuloventa')
router.register('movimientos', movimientoInventarioViewSet, basename='movimiento')
router.register('lotes', loteViewSet, basename='lote')
router.register('user', UserViewSet, basename='users')
router.register('sucursales', SucursalViewSet, basename='sucursal')

urlpatterns = router.urls
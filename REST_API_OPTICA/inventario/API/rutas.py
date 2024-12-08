from rest_framework.routers import DefaultRouter
from inventario.API.vistas import categoriaViewSet, productoViewSet, proveedorViewSet, productoProveedorViewSet, clienteViewSet, ventaViewSet, articuloVentaViewSet, movimientoInventarioViewSet, loteViewSet, UserViewSet, SucursalViewSet

router = DefaultRouter()
router.register('categorias', categoriaViewSet, basename='categoria')
urlpatterns = router.urls 

router.register('productos', productoViewSet, basename='producto')
urlpatterns = router.urls 

router.register('proveedores', proveedorViewSet, basename='proveedor')
urlpatterns = router.urls 

router.register('productoproveedor', productoProveedorViewSet, basename='productoproveedor')
urlpatterns = router.urls 

router.register('clientes', clienteViewSet, basename='cliente')
urlpatterns = router.urls 

router.register('ventas', ventaViewSet, basename='venta')
urlpatterns = router.urls 

router.register('articuloventa', articuloVentaViewSet, basename='articuloventa')
urlpatterns = router.urls 

router.register('movimientos', movimientoInventarioViewSet, basename='movimiento')
urlpatterns = router.urls 

router.register('lotes', loteViewSet, basename='lote')
urlpatterns = router.urls 

router.register('user',UserViewSet, basename= 'users')
urlpatterns = router.urls

router.register('sucursales', SucursalViewSet, basename= 'sucursal')
urlpatterns = router.urls
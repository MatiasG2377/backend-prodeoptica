from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, MovimientoInventario, Lote
from inventario.API.serializers import (
    categoriaSerializer,
    proveedorSerializer,
    ProductoSerializer,
    ProductoProveedorSerializer,
    MovimientoInventarioSerializer,
    LoteSerializer,
)
from inventario.selectors import buscar_productos


class categoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = categoriaSerializer


class productoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        productos = self.get_queryset().filter(Q(estado_producto='Disponible') | Q(cantidad_producto__gt=0))
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filtrar_por_categoria(self, request):
        categoria_id = request.query_params.get('categoria')
        if not categoria_id:
            return Response(self.get_serializer(self.get_queryset(), many=True).data)
        productos = self.get_queryset().filter(categoria_producto_id=categoria_id)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        query = request.query_params.get('q') or request.query_params.get('query', '')
        if not query:
            return Response(self.get_serializer(self.get_queryset(), many=True).data)
        productos = self.get_queryset().filter(
            Q(nombre_producto__icontains=query) |
            Q(descripcion_producto__icontains=query) |
            Q(marca_producto__icontains=query)
        )
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)


class proveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = proveedorSerializer


class productoProveedorViewSet(viewsets.ModelViewSet):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductoProveedorSerializer


class movimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all().order_by('-fecha_movimientoInventario')
    serializer_class = MovimientoInventarioSerializer

    @action(detail=False, methods=['get'], url_path='historial/(?P<producto_id>[^/.]+)')
    def historial(self, request, producto_id=None):
        movimientos = self.get_queryset().filter(producto_movimientoInventario_id=producto_id)
        serializer = self.get_serializer(movimientos, many=True)
        return Response(serializer.data)


class loteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer


class BuscarProductoView(APIView):
    """
    Vista para buscar productos por nombre o descripción.
    """
    def get(self, request):
        query = request.query_params.get('query', None)
        if not query:
            return Response(
                {"detail": "El parámetro 'query' es requerido para realizar una búsqueda."},
                status=status.HTTP_400_BAD_REQUEST
            )

        productos = buscar_productos(query)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

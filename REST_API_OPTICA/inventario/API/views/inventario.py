from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

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


class proveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = proveedorSerializer


class productoProveedorViewSet(viewsets.ModelViewSet):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductoProveedorSerializer


class movimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer


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

from rest_framework import viewsets

from inventario.models import Cliente, Venta, ArticuloVenta
from inventario.API.serializers import clienteSerializer, VentaSerializer, ArticuloVentaSerializer


class clienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = clienteSerializer


class ventaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer


class articuloVentaViewSet(viewsets.ModelViewSet):
    queryset = ArticuloVenta.objects.all()
    serializer_class = ArticuloVentaSerializer

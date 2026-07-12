from rest_framework import viewsets
from inventario.models import Categoria, Proveedor, Producto, ProductoProveedor, Cliente, Venta, ArticuloVenta, MovimientoInventario, Lote, User, Sucursal
from inventario.API.serializador import categoriaSerializer, ProductoSerializer, proveedorSerializer, ProductoProveedorSerializer, clienteSerializer, VentaSerializer, ArticuloVentaSerializer, MovimientoInventarioSerializer, LoteSerializer, UserSerializer, UserSerializer, SucursalSerializer
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

#----------------------- Permisos ------------------
from rest_framework.permissions import IsAuthenticated
from inventario.API.permissions import IsAdministrador, IsGerente, IsUsuario, IsAdminOrManager
from django.contrib.auth import get_user_model
User = get_user_model()


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

class clienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = clienteSerializer

class ventaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class articuloVentaViewSet(viewsets.ModelViewSet):
    queryset = ArticuloVenta.objects.all()
    serializer_class = ArticuloVentaSerializer

class movimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class loteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer


class RegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]  # Solo Administradores o Gerentes pueden registrar

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        # Verificar si el 'refresh_token' está presente en el cuerpo de la solicitud
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Invalidar el token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

#! - - - - - - - - - - Busquedas - - - - - - - - - -

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # Importa Q para consultas avanzadas
from inventario.models import Producto
from inventario.API.serializador import ProductoSerializer

class BuscarProductoView(APIView):
    """
    Vista para buscar productos por nombre o descripción.
    """
    def get(self, request):
        query = request.query_params.get('query', None)  # Obtén el parámetro de búsqueda desde la URL
        if not query:
            return Response(
                {"detail": "El parámetro 'query' es requerido para realizar una búsqueda."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrar productos por nombre o descripción que contengan el término de búsqueda
        productos = Producto.objects.filter(
            Q(nombre_producto__icontains=query) | Q(descripcion_producto__icontains=query)
        )
        
        # Serializar los datos
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



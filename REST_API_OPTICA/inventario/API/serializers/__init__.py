from .usuarios import UserSerializer, SucursalSerializer, CustomTokenObtainPairSerializer
from .inventario import (
    categoriaSerializer,
    proveedorSerializer,
    ProductoSerializer,
    ProductoProveedorSerializer,
    MovimientoInventarioSerializer,
    LoteSerializer,
)
from .ventas import (
    LaboratorioSerializer,
    clienteSerializer,
    PacienteSerializer,
    FichaMedicaSerializer,
    VentaSerializer,
    ArticuloVentaSerializer,
    AbonoSerializer,
    EgresoSerializer,
)

__all__ = [
    'UserSerializer',
    'SucursalSerializer',
    'CustomTokenObtainPairSerializer',
    'categoriaSerializer',
    'proveedorSerializer',
    'ProductoSerializer',
    'ProductoProveedorSerializer',
    'MovimientoInventarioSerializer',
    'LoteSerializer',
    'LaboratorioSerializer',
    'clienteSerializer',
    'PacienteSerializer',
    'FichaMedicaSerializer',
    'VentaSerializer',
    'ArticuloVentaSerializer',
    'AbonoSerializer',
    'EgresoSerializer',
]

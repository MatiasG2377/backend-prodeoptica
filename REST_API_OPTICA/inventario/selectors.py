from django.db.models import Q

from inventario.models import Producto


def buscar_productos(query):
    return Producto.objects.filter(
        Q(nombre_producto__icontains=query) | Q(descripcion_producto__icontains=query)
    )

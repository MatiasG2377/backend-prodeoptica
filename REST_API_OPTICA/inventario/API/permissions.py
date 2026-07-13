from rest_framework.permissions import BasePermission

class IsAdministrador(BasePermission):
    """
    Permite acceso solo a usuarios con rol 'Administrador'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'Administrador'


class IsGerente(BasePermission):
    """
    Permite acceso solo a usuarios con rol 'Gerente'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'Gerente'


class IsUsuario(BasePermission):
    """
    Permite acceso solo a usuarios con rol 'Usuario'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'Usuario'

from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    """
    Permite acceso solo a usuarios con rol 'Administrador' o 'Gerente'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in ['Administrador', 'Gerente']

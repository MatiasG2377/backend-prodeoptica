from django.contrib import admin
from django.urls import path, include
from inventario.API.views import BuscarProductoView

urlpatterns = [
    path('api/', include('inventario.API.JWT.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('inventario.API.urls')),
    path('api/buscar/', BuscarProductoView.as_view(), name='buscar-producto')
]

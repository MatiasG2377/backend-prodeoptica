from django.contrib import admin
from django.urls import path, include
from inventario.API.views import BuscarProductoView
from inventario.views_errors import custom_404, custom_500

urlpatterns = [
    path('api/', include('inventario.API.JWT.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('inventario.API.urls')),
    path('api/buscar/', BuscarProductoView.as_view(), name='buscar-producto')
]

handler404 = custom_404
handler500 = custom_500

from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from inventario.API.views import RegisterView, LogoutView, CustomTokenObtainPairView

urlpatterns = [
    # Login - obtener tokens (access y refresh) y datos del usuario
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refrescar token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Logout - invalidar token
    path('logout/', LogoutView.as_view(), name='logout'),
    # Registro
    path('register/', RegisterView.as_view(), name='register'),
]

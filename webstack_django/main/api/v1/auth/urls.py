from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    ChangePasswordView,
    UpdateProfileView,
    ProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update-profile/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('profile/', ProfileView.as_view(), name='auth_profile'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .views.auth import (
    login, register, request_password_reset,
    reset_password, verify_email
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

app_name = 'main'

urlpatterns = [
    # Auth endpoints
    path('auth/login/', login, name='login'),
    path('auth/register/', register, name='register'),
    path('auth/password-reset/', request_password_reset, name='password-reset'),
    path('auth/password-reset/confirm/', reset_password, name='password-reset-confirm'),
    path('auth/verify-email/', verify_email, name='verify-email'),
    
    # API Root
    path('', include(router.urls)),
]

# Configuration des médias en développement
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

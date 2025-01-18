from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, test_connection

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

app_name = 'main'

urlpatterns = [
    # API Root
    path('', include(router.urls)),
    path('test/', test_connection, name='test-connection'),
]

# Configuration des médias en développement
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

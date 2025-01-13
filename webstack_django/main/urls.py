from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.home_views import home, api_home
from .views.transaction_views import (
    create_transaction,
    process_payment,
    transaction_history,
    transaction_details
)
from . import api_views, auth_views

app_name = 'main'

# Configuration du routeur DRF
router = DefaultRouter()

urlpatterns = [
    # Pages principales
    path('', home, name='home'),
    
    # API Endpoints
    path('api/', api_home, name='api_home'),
    
    # API Authentification
    path('api/auth/login/', auth_views.login_view, name='api_login'),
    path('api/auth/register/', auth_views.register_view, name='api_register'),
    path('api/auth/logout/', auth_views.logout_view, name='api_logout'),
    
    # API Produits
    path('api/products/', api_views.get_products, name='get_products'),
    path('api/products/<str:product_id>/', api_views.get_product_details, name='get_product_details'),
    path('api/products/create/', api_views.create_product, name='create_product'),

    # API Transactions
    path('api/transactions/create/', create_transaction, name='create_transaction'),
    path('api/transactions/process/<str:transaction_id>/', process_payment, name='process_payment'),
    path('api/transactions/history/', transaction_history, name='transaction_history'),
    path('api/transactions/<str:transaction_id>/', transaction_details, name='transaction_details'),
]

# Ajout des URLs du routeur DRF
urlpatterns += router.urls

# Configuration des médias en développement
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

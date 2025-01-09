from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import auth_views
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'main'

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='product')

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/search/', views.product_search, name='product_search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('search/', views.search_view, name='search'),  # Ajout de l'URL de recherche
    
    # Profil utilisateur
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('orders/', views.order_list, name='order_list'),
    
    # Authentification
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # API endpoints (pour les requêtes AJAX)
    path('api/', include(router.urls)),
    path('api/products/<slug:slug>/', views.api_product_detail, name='api_product_detail'),
    path('api/categories/', views.api_category_list, name='api_category_list'),
    path('api/categories/<slug:slug>/', views.api_category_detail, name='api_category_detail'),
    path('api/search/', views.api_search, name='api_search'),  # Ajout de l'API de recherche
]

# Ajout des URLs pour servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from . import auth_views

app_name = 'main'

urlpatterns = [
    path('', views.product_list, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:product_slug>/review/', views.add_review, name='add_review'),
    path('search/', views.search, name='search'),
    
    # Authentication URLs
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
]

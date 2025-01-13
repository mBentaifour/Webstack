from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    PaymentViewSet,
    ProductViewSet,
    CategoryViewSet,
    BrandViewSet,
)
from .webhooks import stripe_webhook

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]

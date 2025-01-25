"""
URL configuration for webstack_django project.
"""
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "healthy"})


urlpatterns = [
    path('', include('core.urls')),
    path('api/health/', health_check, name='health_check'),
    path('api/auth/', include('auth_.urls')),
]

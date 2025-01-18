"""
URL configuration for webstack_django project.
"""
from django.contrib import admin
from django.urls import path, include
from core.views import index
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    return Response({"status": "healthy"})

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/health/', health_check, name='health_check'),
]

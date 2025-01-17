"""
URL configuration for webstack_django project.
"""
from django.contrib import admin
from django.urls import path, include
from core.views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
]

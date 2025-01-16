from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Product, Category

def home(request):
    """Vue de la page d'accueil"""
    context = {
        'featured_products': Product.objects.filter(featured=True)[:4],
        'categories': Category.objects.filter(parent=None)[:6]
    }
    return render(request, 'main/home.html', context)

@api_view(['GET'])
def api_home(request):
    """API endpoint pour la page d'accueil"""
    return Response({
        'message': 'Bienvenue sur l\'API de notre e-commerce',
        'version': '1.0',
        'endpoints': {
            'products': '/api/products/',
            'categories': '/api/categories/',
            'transactions': '/api/transactions/',
        }
    })

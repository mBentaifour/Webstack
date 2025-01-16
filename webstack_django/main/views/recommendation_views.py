from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.base_models import Product, Category, Brand
from ..models.order import Order, OrderItem
from ..serializers import ProductSerializer
from django.db.models import Count, Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personalized_recommendations(request):
    """Retourne des recommandations personnalisées basées sur l'historique de l'utilisateur"""
    user = request.user
    # Obtenir les catégories préférées de l'utilisateur
    favorite_categories = Product.objects.filter(
        order_items__order__user=user
    ).values('category').annotate(count=Count('id')).order_by('-count')[:5]
    
    # Obtenir les produits des catégories préférées
    recommended_products = Product.objects.filter(
        category__in=[cat['category'] for cat in favorite_categories]
    ).exclude(
        order_items__order__user=user
    )[:10]
    
    serializer = ProductSerializer(recommended_products, many=True)
    return Response({'products': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_similar_products(request, product_id):
    """Retourne des produits similaires à un produit donné"""
    try:
        product = Product.objects.get(id=product_id)
        similar_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:5]
        serializer = ProductSerializer(similar_products, many=True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brand_recommendations(request, brand_id):
    """Retourne des recommandations basées sur une marque"""
    try:
        brand = Brand.objects.get(id=brand_id)
        recommended_products = Product.objects.filter(brand=brand)[:10]
        serializer = ProductSerializer(recommended_products, many=True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)
    except Brand.DoesNotExist:
        return Response(
            {'error': 'Brand not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_recommendations(request, category_id):
    """Retourne des recommandations basées sur une catégorie"""
    try:
        category = Category.objects.get(id=category_id)
        recommended_products = Product.objects.filter(category=category)[:10]
        serializer = ProductSerializer(recommended_products, many=True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response(
            {'error': 'Category not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_price_range_recommendations(request):
    """Retourne des recommandations basées sur une gamme de prix"""
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', float('inf'))
    
    recommended_products = Product.objects.filter(
        price__gte=min_price,
        price__lte=max_price
    ).order_by('price')[:10]
    
    serializer = ProductSerializer(recommended_products, many=True)
    return Response({'products': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_trending_products(request):
    """Retourne les produits tendance basés sur les commandes récentes"""
    trending_products = Product.objects.annotate(
        order_count=Count('order_items')
    ).order_by('-order_count')[:10]
    
    serializer = ProductSerializer(trending_products, many=True)
    return Response({'products': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recently_viewed(request):
    """Retourne les produits récemment consultés par l'utilisateur"""
    # Cette fonctionnalité nécessiterait un modèle pour suivre les produits consultés
    # Pour l'instant, nous retournons simplement les derniers produits créés
    recent_products = Product.objects.order_by('-created_at')[:10]
    serializer = ProductSerializer(recent_products, many=True)
    return Response({'products': serializer.data}, status=status.HTTP_200_OK)

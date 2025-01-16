import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Brand
from .auth_manager import AuthManager, require_auth
from main.decorators import supabase_auth_required
import json
import os
from rest_framework import viewsets
from .serializers import ProductSerializer

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_manager = AuthManager()

def home(request):
    """Page d'accueil"""
    try:
        # Récupérer les catégories principales avec gestion des erreurs
        try:
            categories = Category.objects.all()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des catégories: {str(e)}")
            categories = []
        
        # Récupérer les produits en vedette avec gestion des erreurs
        try:
            featured_products = Product.objects.all()[:6]  # Limiter à 6 produits
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
            featured_products = []
        
        context = {
            'categories': categories,
            'featured_products': featured_products
        }
        
        return render(request, 'main/home.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page d'accueil: {str(e)}")
        messages.error(request, "Une erreur est survenue lors du chargement de la page.")
        return render(request, 'main/home.html', {'categories': [], 'featured_products': []})

@supabase_auth_required
def product_list(request):
    """
    Vue pour la liste des produits.
    """
    products = Product.objects.all()
    
    # Filtres
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    usage_type = request.GET.get('usage_type')
    power_source = request.GET.get('power_source')
    min_warranty = request.GET.get('min_warranty')
    
    if category:
        products = products.filter(category__category_type=category)
    if brand:
        products = products.filter(brand__name=brand)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if usage_type:
        products = products.filter(usage_type=usage_type)
    if power_source:
        products = products.filter(power_source=power_source)
    if min_warranty:
        products = products.filter(warranty_duration__gte=min_warranty)
    
    context = {
        'products': products,
        'category': category,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'usage_type': usage_type,
        'power_source': power_source,
        'min_warranty': min_warranty
    }
    
    return render(request, 'main/product_list.html', context)

@supabase_auth_required
def product_detail(request, slug):
    """
    Vue pour le détail d'un produit.
    """
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'main/product_detail.html', context)

def category_list(request):
    """Liste des catégories"""
    try:
        categories = Category.objects.all()
        
        context = {
            'categories': categories
        }
        
        return render(request, 'main/category_list.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage des catégories: {str(e)}")
        messages.error(request, "Une erreur est survenue lors du chargement des catégories.")
        return render(request, 'main/category_list.html', {'categories': []})

def category_detail(request, slug):
    """Détails d'une catégorie"""
    try:
        category = get_object_or_404(Category, slug=slug)
        
        # Récupérer les produits de la catégorie
        products = Product.objects.filter(category=category)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        paginator = Paginator(products, 12)  # 12 produits par page
        page_obj = paginator.get_page(page)
        
        context = {
            'category': category,
            'products': page_obj
        }
        
        return render(request, 'main/category_detail.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage de la catégorie {slug}: {str(e)}")
        messages.error(request, "Une erreur est survenue lors du chargement de la catégorie.")
        return redirect('main:category_list')

@require_auth
def profile(request):
    """Profil utilisateur"""
    try:
        user_id = request.user.id
        
        # Récupérer les commandes de l'utilisateur
        orders = Order.objects.filter(user=user_id)
        
        context = {
            'orders': orders
        }
        
        return render(request, 'main/profile.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage du profil: {str(e)}")
        messages.error(request, "Une erreur est survenue lors du chargement du profil.")
        return render(request, 'main/profile.html', {})

@require_auth
def edit_profile(request):
    if request.method == 'POST':
        # Logique de mise à jour du profil
        messages.success(request, 'Profil mis à jour avec succès')
        return redirect('main:profile')
    return render(request, 'main/edit_profile.html')

@require_auth
def dashboard(request):
    return render(request, 'main/dashboard.html')

@require_auth
def stock_alerts(request):
    alerts = StockAlert.objects.all()
    return render(request, 'main/stock_alerts.html', {'alerts': alerts})

@require_auth
def process_stock_alert(request, alert_id):
    if request.method == 'POST':
        alert = get_object_or_404(StockAlert, pk=alert_id)
        alert.processed = True
        alert.save()
        messages.success(request, 'Alerte traitée avec succès')
    return redirect('main:stock_alerts')

@require_auth
def check_stock_levels(request):
    products = Product.objects.all()
    for product in products:
        if product.stock < product.min_stock:
            StockAlert.objects.create(product=product)
    messages.success(request, 'Niveaux de stock vérifiés avec succès')
    return redirect('main:stock_alerts')

@require_auth
def add_review(request, product_slug):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, slug=product_slug)
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )
            messages.success(request, "Votre avis a été ajouté avec succès")
        else:
            messages.error(request, "Erreur lors de l'ajout de l'avis")
    return redirect('product_detail', slug=product_slug)

@require_auth
def order_list(request):
    user = request.user
    
    # Pagination
    page = int(request.GET.get('page', 1))
    items_per_page = 10
    offset = (page - 1) * items_per_page
    
    # Récupérer les commandes
    orders = Order.objects.filter(user=user).order_by('-date')[offset:offset+items_per_page]
    
    context = {
        'orders': orders,
        'page': page
    }
    return render(request, 'main/order_list.html', context)

@require_auth
def order_detail(request, order_id):
    user = request.user
    
    # Récupérer les détails de la commande
    order = get_object_or_404(Order, pk=order_id, user=user)
    
    context = {
        'order': order
    }
    return render(request, 'main/order_detail.html', context)

@require_auth
def notification_list(request):
    user = request.user
    
    # Pagination
    page = int(request.GET.get('page', 1))
    items_per_page = 20
    offset = (page - 1) * items_per_page
    
    # Récupérer les notifications
    notifications = Notification.objects.filter(user=user).order_by('-date')[offset:offset+items_per_page]
    
    context = {
        'notifications': notifications,
        'page': page
    }
    return render(request, 'main/notification_list.html', context)

@require_auth
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
        notification.read = True
        notification.save()
        messages.success(request, 'Notification marquée comme lue')
    return redirect('main:notifications')

@require_auth
def product_list(request):
    """Vue pour afficher la liste des produits."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    # Paramètres de filtrage et pagination
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    search = request.GET.get('q')
    page = int(request.GET.get('page', 1))
    include_inactive = request.GET.get('include_inactive') == '1'
    
    # Cache key pour les filtres
    cache_key = f"products_{category_id}_{brand_id}_{search}_{include_inactive}_{page}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        products = cached_data
    else:
        products = Product.objects.all()
        
        # Filtrer par catégorie si spécifié
        if category_id:
            products = products.filter(category=category_id)
        
        # Filtrer par marque si spécifié
        if brand_id:
            products = products.filter(brand=brand_id)
        
        # Filtrer par recherche si spécifié
        if search:
            search = search.lower()
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
        
        # Pagination
        paginator = Paginator(products, 12)  # 12 produits par page
        page_obj = paginator.get_page(page)
        
        # Récupérer les catégories pour le filtre
        categories = Category.objects.all()
        
        context = {
            'products': page_obj,
            'categories': categories,
            'current_category': category_id,
            'current_brand': brand_id,
            'search_query': search,
            'include_inactive': include_inactive,
            'page_title': 'Gestion des produits'
        }
        cache.set(cache_key, products, 300)  # Cache pour 5 minutes
        return render(request, 'main/product_list.html', context)

@require_auth
def product_detail(request, product_id):
    """Vue pour afficher/modifier un produit."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        # Traiter la mise à jour du produit
        data = request.POST.dict()
        files = request.FILES
        
        # Ajouter les fichiers au dictionnaire de données
        if 'image' in files:
            data['image'] = files['image']
        if 'additional_images' in files:
            data['additional_images'] = files.getlist('additional_images')
        
        # Ajouter l'ID de l'utilisateur
        data['updated_by'] = request.user.id
        
        # Convertir les valeurs numériques
        for field in ['price', 'stock', 'min_stock', 'max_stock', 'weight']:
            if field in data:
                try:
                    data[field] = float(data[field])
                except (ValueError, TypeError):
                    data[field] = 0
        
        # Mettre à jour le produit
        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.stock = data['stock']
        product.min_stock = data['min_stock']
        product.max_stock = data['max_stock']
        product.weight = data['weight']
        product.save()
        
        messages.success(request, "Produit mis à jour avec succès.")
        return redirect('main:product_list')
    
    context = {
        'product': product,
        'page_title': f'Modifier {product.name}'
    }
    return render(request, 'main/product_detail.html', context)

@require_auth
def product_create(request):
    """Vue pour créer un nouveau produit."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    if request.method == 'POST':
        data = request.POST.dict()
        files = request.FILES
        
        # Ajouter les fichiers au dictionnaire de données
        if 'image' in files:
            data['image'] = files['image']
        if 'additional_images' in files:
            data['additional_images'] = files.getlist('additional_images')
        
        # Ajouter l'ID de l'utilisateur
        data['created_by'] = request.user.id
        
        # Convertir les valeurs numériques
        for field in ['price', 'stock', 'min_stock', 'max_stock', 'weight']:
            if field in data:
                try:
                    data[field] = float(data[field])
                except (ValueError, TypeError):
                    data[field] = 0
        
        # Créer le produit
        product = Product.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            min_stock=data['min_stock'],
            max_stock=data['max_stock'],
            weight=data['weight'],
            created_by=request.user
        )
        
        messages.success(request, "Produit créé avec succès.")
        return redirect('main:product_list')
    
    context = {
        'page_title': 'Nouveau produit'
    }
    return render(request, 'main/product_form.html', context)

@require_auth
def category_list(request):
    """Vue pour afficher la liste des catégories."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'page_title': 'Gestion des catégories'
    }
    return render(request, 'main/category_list.html', context)

@require_auth
def category_create(request):
    """Vue pour créer une nouvelle catégorie."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    if request.method == 'POST':
        data = request.POST.dict()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']
        
        # Créer la catégorie
        category = Category.objects.create(
            name=data['name'],
            description=data['description'],
            image=data.get('image')
        )
        
        messages.success(request, "Catégorie créée avec succès.")
        return redirect('main:category_list')
    
    context = {
        'page_title': 'Nouvelle catégorie'
    }
    return render(request, 'main/category_form.html', context)

@require_auth
def category_edit(request, category_id):
    """Vue pour modifier une catégorie."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        data = request.POST.dict()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']
        
        # Mettre à jour la catégorie
        category.name = data['name']
        category.description = data['description']
        category.image = data.get('image')
        category.save()
        
        messages.success(request, "Catégorie mise à jour avec succès.")
        return redirect('main:category_list')
    
    context = {
        'category': category,
        'page_title': f'Modifier {category.name}'
    }
    return render(request, 'main/category_form.html', context)

@csrf_protect
@require_http_methods(["POST"])
def login(request):
    """Vue de connexion"""
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            return JsonResponse({
                "success": False,
                "error": "Email et mot de passe requis"
            }, status=400)
        
        result = auth_manager.login(email, password)
        
        if result["success"]:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=401)
            
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

@require_auth
@require_http_methods(["GET"])
def get_user_profile(request):
    """Récupère le profil de l'utilisateur connecté"""
    try:
        user_id = request.user.id
        profile = {
            'success': True,
            'data': {
                'id': user_id,
                'email': request.user.email,
                'name': request.user.username
            }
        }
        
        return JsonResponse(profile)
            
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

@require_http_methods(["GET"])
def api_product_list(request):
    """API endpoint pour la liste des produits"""
    try:
        # Paramètres de filtrage
        category_slug = request.GET.get('category')
        brand_slug = request.GET.get('brand')
        search = request.GET.get('q')
        sort = request.GET.get('sort', 'name')
        
        # Récupérer les produits
        products = Product.objects.all()
        
        # Appliquer les filtres
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        
        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            products = products.filter(brand=brand)
        
        if search:
            search = search.lower()
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
        
        # Trier les produits
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('name')
        
        return JsonResponse({'products': [{'id': p.id, 'name': p.name, 'slug': p.slug, 'price': p.price, 'image': p.image.url if p.image else None} for p in products]})
        
    except Exception as e:
        logger.error(f"Erreur API - Liste des produits: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_product_detail(request, slug):
    """API endpoint pour les détails d'un produit"""
    try:
        product = get_object_or_404(Product, slug=slug)
        
        return JsonResponse({
            'product': {
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'price': product.price,
                'image': product.image.url if product.image else None,
                'description': product.description
            }
        })
        
    except Exception as e:
        logger.error(f"Erreur API - Détails du produit: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_category_list(request):
    """API endpoint pour la liste des catégories"""
    try:
        categories = Category.objects.all()
        return JsonResponse({'categories': [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in categories]})
        
    except Exception as e:
        logger.error(f"Erreur API - Liste des catégories: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_category_detail(request, slug):
    """API endpoint pour les détails d'une catégorie"""
    try:
        category = get_object_or_404(Category, slug=slug)
        
        return JsonResponse({
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'description': category.description
            }
        })
        
    except Exception as e:
        logger.error(f"Erreur API - Détails de la catégorie: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def search_view(request):
    """Vue pour la page de recherche"""
    query = request.GET.get('q', '')
    
    if query:
        # Recherche dans les produits
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = []
    
    context = {
        'query': query,
        'products': products,
        'title': f'Recherche: {query}' if query else 'Recherche'
    }
    
    return render(request, 'main/search.html', context)

@require_http_methods(["GET"])
def api_search(request):
    """API endpoint pour la recherche"""
    query = request.GET.get('q', '')
    
    if not query:
        return JsonResponse({
            'success': False,
            'error': 'Veuillez fournir un terme de recherche'
        })
    
    try:
        # Recherche dans les produits
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
        
        # Sérialiser les résultats
        products_data = [{'id': p.id, 'name': p.name, 'slug': p.slug, 'price': p.price, 'image': p.image.url if p.image else None} for p in products]
        
        return JsonResponse({
            'success': True,
            'data': {
                'products': products_data,
                'count': len(products_data)
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@supabase_auth_required
def product_search(request):
    """
    Vue pour la recherche avancée de produits.
    """
    # Récupération des paramètres de recherche
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    usage_type = request.GET.get('usage_type', '')
    power_source = request.GET.get('power_source', '')
    
    # Construction du queryset de base
    products = Product.objects.all()
    
    # Application des filtres
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(usage_type__icontains=query)
        )
    
    if category:
        products = products.filter(category__category_type=category)
    
    if brand:
        products = products.filter(brand__name=brand)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if usage_type:
        products = products.filter(usage_type=usage_type)
    
    if power_source:
        products = products.filter(power_source=power_source)
    
    # Préparation du contexte
    context = {
        'products': products,
        'query': query,
        'category': category,
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'usage_type': usage_type,
        'power_source': power_source
    }
    
    # Utilisation du template de test en mode test
    template = 'main/test_search.html' if os.environ.get('TESTING') == 'True' else 'main/product_search.html'
    
    return render(request, template, context)

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

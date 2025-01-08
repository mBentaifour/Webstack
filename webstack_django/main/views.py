import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .supabase_adapter import SupabaseAdapter
from .auth_manager import AuthManager, require_auth
import json

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_manager = AuthManager()
supabase_adapter = SupabaseAdapter()

def home(request):
    """Page d'accueil"""
    try:
        db = supabase_adapter
        
        # Récupérer les catégories principales avec gestion des erreurs
        try:
            categories = db.get_categories()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des catégories: {str(e)}")
            categories = []
        
        # Récupérer les produits en vedette avec gestion des erreurs
        try:
            featured_products = db.get_products()[:6]  # Limiter à 6 produits
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

def product_list(request):
    """Liste des produits avec filtres"""
    try:
        db = supabase_adapter
        
        # Paramètres de filtrage
        category_slug = request.GET.get('category')
        brand_slug = request.GET.get('brand')
        search = request.GET.get('q')
        sort = request.GET.get('sort', 'name')  # Tri par nom par défaut
        page = int(request.GET.get('page', 1))
        
        # Récupérer les IDs des catégories et marques si les slugs sont fournis
        category_id = None
        if category_slug:
            category = db.get_category_by_slug(category_slug)
            if category:
                category_id = category['id']
        
        brand_id = None
        if brand_slug:
            brand = db.get_brand_by_slug(brand_slug)
            if brand:
                brand_id = brand['id']
        
        # Récupérer les produits filtrés
        products = db.get_products()
        
        # Filtrer par catégorie si spécifié
        if category_id:
            products = [p for p in products if p['category_id'] == category_id]
        
        # Filtrer par marque si spécifié
        if brand_id:
            products = [p for p in products if p['brand_id'] == brand_id]
        
        # Filtrer par recherche si spécifié
        if search:
            search = search.lower()
            products = [p for p in products if search in p['name'].lower() or 
                       (p['description'] and search in p['description'].lower())]
        
        # Trier les produits
        if sort == 'price_asc':
            products.sort(key=lambda x: float(x['price']))
        elif sort == 'price_desc':
            products.sort(key=lambda x: float(x['price']), reverse=True)
        else:  # Par nom par défaut
            products.sort(key=lambda x: x['name'])
        
        # Pagination
        paginator = Paginator(products, 12)  # 12 produits par page
        page_obj = paginator.get_page(page)
        
        # Récupérer les catégories et marques pour les filtres
        categories = db.get_categories()
        brands = db.get_brands()
        
        context = {
            'products': page_obj,
            'categories': categories,
            'brands': brands,
            'current_category': category_slug,
            'current_brand': brand_slug,
            'current_sort': sort,
            'search_query': search
        }
        
        return render(request, 'main/product_list.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage des produits: {str(e)}")
        messages.error(request, "Une erreur est survenue lors du chargement des produits.")
        return render(request, 'main/product_list.html', {'products': []})

def product_detail(request, slug):
    """Détails d'un produit"""
    try:
        db = supabase_adapter
        product = db.get_product_by_slug(slug)
        
        if not product:
            messages.error(request, "Ce produit n'existe pas.")
            return redirect('main:product_list')
        
        # Récupérer les produits similaires
        similar_products = db.get_similar_products(product['id'], limit=4)
        
        context = {
            'product': product,
            'similar_products': similar_products
        }
        
        return render(request, 'main/product_detail.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'affichage du produit {slug}: {str(e)}")
        messages.error(request, "Une erreur est survenue lors du chargement du produit.")
        return redirect('main:product_list')

def category_list(request):
    """Liste des catégories"""
    try:
        db = supabase_adapter
        categories = db.get_categories()
        
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
        db = supabase_adapter
        category = db.get_category_by_slug(slug)
        
        if not category:
            messages.error(request, "Cette catégorie n'existe pas.")
            return redirect('main:category_list')
        
        # Récupérer les produits de la catégorie
        products = [p for p in db.get_products() if p['category_id'] == category['id']]
        
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
        db = supabase_adapter
        user_id = request.user.id
        
        # Récupérer les commandes de l'utilisateur
        orders = db.get_user_orders(user_id)
        
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
    db = supabase_adapter
    alerts = db.get_stock_alerts()
    return render(request, 'main/stock_alerts.html', {'alerts': alerts})

@require_auth
def process_stock_alert(request, alert_id):
    if request.method == 'POST':
        db = supabase_adapter
        result = db.process_stock_alert(alert_id)
        if result['success']:
            messages.success(request, 'Alerte traitée avec succès')
        else:
            messages.error(request, result.get('error', 'Erreur lors du traitement de l\'alerte'))
    return redirect('main:stock_alerts')

@require_auth
def check_stock_levels(request):
    db = supabase_adapter
    result = db.check_stock_levels()
    if result['success']:
        messages.success(request, 'Niveaux de stock vérifiés avec succès')
    else:
        messages.error(request, result.get('error', 'Erreur lors de la vérification des stocks'))
    return redirect('main:stock_alerts')

@require_auth
def add_review(request, product_slug):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            db = supabase_adapter
            product_data = db.get_product_by_slug(product_slug)
            
            if product_data.get('success'):
                review_data = {
                    'product_id': product_data['data']['id'],
                    'user_id': request.user.id,
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
                
                result = db.add_review(review_data)
                if result.get('success'):
                    messages.success(request, "Votre avis a été ajouté avec succès")
                else:
                    messages.error(request, "Erreur lors de l'ajout de l'avis")
            else:
                messages.error(request, "Produit non trouvé")
    
    return redirect('product_detail', slug=product_slug)

@require_auth
def order_list(request):
    db = supabase_adapter
    user = request.user
    
    # Pagination
    page = int(request.GET.get('page', 1))
    items_per_page = 10
    offset = (page - 1) * items_per_page
    
    # Récupérer les commandes
    orders = db.get_user_orders(user.id, limit=items_per_page, offset=offset)
    
    context = {
        'orders': orders.get('data', []),
        'page': page
    }
    return render(request, 'main/order_list.html', context)

@require_auth
def order_detail(request, order_id):
    db = supabase_adapter
    user = request.user
    
    # Récupérer les détails de la commande
    order = db.get_order_details(order_id, user.id)
    
    if not order['success']:
        raise Http404("Commande non trouvée")
    
    context = {
        'order': order['data']
    }
    return render(request, 'main/order_detail.html', context)

@require_auth
def notification_list(request):
    db = supabase_adapter
    user = request.user
    
    # Pagination
    page = int(request.GET.get('page', 1))
    items_per_page = 20
    offset = (page - 1) * items_per_page
    
    # Récupérer les notifications
    notifications = db.get_notifications(user.id, limit=items_per_page, offset=offset)
    
    context = {
        'notifications': notifications.get('data', []),
        'page': page
    }
    return render(request, 'main/notification_list.html', context)

@require_auth
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        db = supabase_adapter
        user = request.user
        
        result = db.mark_notification_as_read(notification_id, user.id)
        
        if result['success']:
            messages.success(request, 'Notification marquée comme lue')
        else:
            messages.error(request, 'Erreur lors de la mise à jour de la notification')
    
    return redirect('main:notifications')

@require_auth
def product_list(request):
    """Vue pour afficher la liste des produits."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    db = supabase_adapter
    
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
        products = db.get_products(
            category_id=category_id,
            brand_id=brand_id,
            search=search,
            include_inactive=include_inactive,
            page=page
        )
        cache.set(cache_key, products, 300)  # Cache pour 5 minutes
    
    # Récupérer les catégories pour le filtre
    categories_result = db.get_categories(include_inactive=True)
    
    if not products['success']:
        messages.error(request, "Erreur lors de la récupération des produits.")
        return redirect('main:dashboard')
    
    context = {
        'products': products['data']['products'],
        'pagination': products['data']['pagination'],
        'categories': categories_result.get('data', []),
        'current_category': category_id,
        'current_brand': brand_id,
        'search_query': search,
        'include_inactive': include_inactive,
        'page_title': 'Gestion des produits'
    }
    return render(request, 'main/product_list.html', context)

@require_auth
def product_detail(request, product_id):
    """Vue pour afficher/modifier un produit."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    db = supabase_adapter
    
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
        
        result = db.update_product(product_id, data)
        
        if result['success']:
            messages.success(request, "Produit mis à jour avec succès.")
            return redirect('main:product_list')
        else:
            messages.error(request, "Erreur lors de la mise à jour du produit.")
    
    # Récupérer les détails du produit
    product_result = db.get_product(product_id)
    categories_result = db.get_categories(include_inactive=True)
    
    if not product_result['success']:
        messages.error(request, "Erreur lors de la récupération du produit.")
        return redirect('main:product_list')
    
    context = {
        'product': product_result['data'],
        'categories': categories_result.get('data', []),
        'page_title': f'Modifier {product_result["data"]["name"]}'
    }
    return render(request, 'main/product_detail.html', context)

@require_auth
def product_create(request):
    """Vue pour créer un nouveau produit."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    db = supabase_adapter
    
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
        
        result = db.create_product(data)
        
        if result['success']:
            messages.success(request, "Produit créé avec succès.")
            return redirect('main:product_list')
        else:
            messages.error(request, "Erreur lors de la création du produit.")
    
    # Récupérer les catégories pour le formulaire
    categories_result = db.get_categories(include_inactive=True)
    
    context = {
        'categories': categories_result.get('data', []),
        'page_title': 'Nouveau produit'
    }
    return render(request, 'main/product_form.html', context)

@require_auth
def category_list(request):
    """Vue pour afficher la liste des catégories."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    db = supabase_adapter
    tree_result = db.get_category_tree()
    
    if not tree_result['success']:
        messages.error(request, "Erreur lors de la récupération des catégories.")
        return redirect('main:dashboard')
    
    context = {
        'categories': tree_result['data'],
        'page_title': 'Gestion des catégories'
    }
    return render(request, 'main/category_list.html', context)

@require_auth
def category_create(request):
    """Vue pour créer une nouvelle catégorie."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    db = supabase_adapter
    
    if request.method == 'POST':
        data = request.POST.dict()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']
        
        result = db.create_category(data)
        
        if result['success']:
            messages.success(request, "Catégorie créée avec succès.")
            return redirect('main:category_list')
        else:
            messages.error(request, "Erreur lors de la création de la catégorie.")
    
    # Récupérer les catégories parentes possibles
    categories_result = db.get_categories(include_inactive=True)
    
    context = {
        'categories': categories_result.get('data', []),
        'page_title': 'Nouvelle catégorie'
    }
    return render(request, 'main/category_form.html', context)

@require_auth
def category_edit(request, category_id):
    """Vue pour modifier une catégorie."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé.")
        return redirect('main:home')
    
    db = supabase_adapter
    
    if request.method == 'POST':
        data = request.POST.dict()
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']
        
        result = db.update_category(category_id, data)
        
        if result['success']:
            messages.success(request, "Catégorie mise à jour avec succès.")
            return redirect('main:category_list')
        else:
            messages.error(request, "Erreur lors de la mise à jour de la catégorie.")
    
    # Récupérer les détails de la catégorie
    categories_result = db.get_categories(include_inactive=True)
    category_result = db.get_category(category_id)
    
    if not category_result['success']:
        messages.error(request, "Erreur lors de la récupération de la catégorie.")
        return redirect('main:category_list')
    
    context = {
        'category': category_result['data'],
        'categories': categories_result.get('data', []),
        'page_title': f'Modifier {category_result["data"]["name"]}'
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
        profile = supabase_adapter.get_user_profile(user_id)
        
        if profile.get("success"):
            return JsonResponse(profile)
        else:
            return JsonResponse(profile, status=404)
            
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

@require_http_methods(["GET"])
def api_product_list(request):
    """API endpoint pour la liste des produits"""
    try:
        db = supabase_adapter
        
        # Paramètres de filtrage
        category_slug = request.GET.get('category')
        brand_slug = request.GET.get('brand')
        search = request.GET.get('q')
        sort = request.GET.get('sort', 'name')
        
        # Récupérer les produits
        products = db.get_products()
        
        # Appliquer les filtres
        if category_slug:
            category = db.get_category_by_slug(category_slug)
            if category:
                products = [p for p in products if p['category_id'] == category['id']]
        
        if brand_slug:
            brand = db.get_brand_by_slug(brand_slug)
            if brand:
                products = [p for p in products if p['brand_id'] == brand['id']]
        
        if search:
            search = search.lower()
            products = [p for p in products if search in p['name'].lower() or 
                       (p['description'] and search in p['description'].lower())]
        
        # Trier les produits
        if sort == 'price_asc':
            products.sort(key=lambda x: float(x['price']))
        elif sort == 'price_desc':
            products.sort(key=lambda x: float(x['price']), reverse=True)
        else:
            products.sort(key=lambda x: x['name'])
        
        return JsonResponse({'products': products})
        
    except Exception as e:
        logger.error(f"Erreur API - Liste des produits: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_product_detail(request, slug):
    """API endpoint pour les détails d'un produit"""
    try:
        db = supabase_adapter
        product = db.get_product_by_slug(slug)
        
        if not product:
            return JsonResponse({'error': 'Produit non trouvé'}, status=404)
        
        # Récupérer les produits similaires
        similar_products = db.get_similar_products(product['id'], limit=4)
        
        return JsonResponse({
            'product': product,
            'similar_products': similar_products
        })
        
    except Exception as e:
        logger.error(f"Erreur API - Détails du produit: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_category_list(request):
    """API endpoint pour la liste des catégories"""
    try:
        db = supabase_adapter
        categories = db.get_categories()
        return JsonResponse({'categories': categories})
        
    except Exception as e:
        logger.error(f"Erreur API - Liste des catégories: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def api_category_detail(request, slug):
    """API endpoint pour les détails d'une catégorie"""
    try:
        db = supabase_adapter
        category = db.get_category_by_slug(slug)
        
        if not category:
            return JsonResponse({'error': 'Catégorie non trouvée'}, status=404)
        
        # Récupérer les produits de la catégorie
        products = [p for p in db.get_products() if p['category_id'] == category['id']]
        
        return JsonResponse({
            'category': category,
            'products': products
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
        products = cache.get(f'search_products_{query}')
        if products is None:
            products = db.get_products(
                search=query
            )
            cache.set(f'search_products_{query}', products, 300)  # Cache pour 5 minutes
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
        products = cache.get(f'search_products_{query}')
        if products is None:
            products = db.get_products(
                search=query
            )
            cache.set(f'search_products_{query}', products, 300)  # Cache pour 5 minutes
        
        # Sérialiser les résultats
        products_data = [{
            'id': p['id'],
            'name': p['name'],
            'slug': p['slug'],
            'price': str(p['price']),
            'image_url': p.get('image', {}).get('url') if p.get('image') else None,
            'category': p.get('category', {}).get('name') if p.get('category') else None
        } for p in products]
        
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

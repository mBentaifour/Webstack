from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .forms import ReviewForm
from .supabase_adapter import SupabaseAdapter

def product_list(request):
    db = SupabaseAdapter()
    
    # Récupérer les paramètres de pagination
    page = request.GET.get('page', 1)
    items_per_page = 12
    offset = (int(page) - 1) * items_per_page
    
    # Récupérer les produits depuis Supabase
    products = db.get_products(limit=items_per_page, offset=offset)
    categories = db.get_categories()
    brands = db.get_brands()
    
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    
    return render(request, 'main/product_list.html', context)

def product_detail(request, slug):
    db = SupabaseAdapter()
    product = db.get_product_by_slug(slug)
    
    if not product:
        raise Http404("Produit non trouvé")
    
    reviews = db.get_reviews_by_product(product['id'])
    review_form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form
    }
    
    return render(request, 'main/product_detail.html', context)

def category_list(request):
    db = SupabaseAdapter()
    categories = db.get_categories()
    return render(request, 'main/category_list.html', {'categories': categories})

def category_detail(request, slug):
    db = SupabaseAdapter()
    categories = db.get_categories()
    category = next((cat for cat in categories if cat['slug'] == slug), None)
    
    if not category:
        raise Http404("Catégorie non trouvée")
    
    products = db.get_products()  # À améliorer avec un filtre par catégorie
    products = [p for p in products if p['category_id'] == category['id']]
    
    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products
    })

@login_required
def add_review(request, product_slug):
    db = SupabaseAdapter()
    product = db.get_product_by_slug(product_slug)
    
    if not product:
        raise Http404("Produit non trouvé")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_data = {
                'product_id': product['id'],
                'user_id': str(request.user.id),  # Convertir en string car UUID
                'rating': form.cleaned_data['rating'],
                'comment': form.cleaned_data['comment']
            }
            
            review = db.create_review(review_data)
            if review:
                messages.success(request, 'Votre avis a été ajouté avec succès!')
            else:
                messages.error(request, 'Une erreur est survenue lors de l\'ajout de votre avis.')
                
    return redirect('product_detail', slug=product_slug)

def search(request):
    db = SupabaseAdapter()
    query = request.GET.get('q', '')
    
    if query:
        # Pour l'instant, on récupère tous les produits et on filtre côté Python
        # À améliorer avec une recherche côté Supabase
        all_products = db.get_products(limit=100)  # Augmenter la limite pour la recherche
        products = [
            p for p in all_products 
            if query.lower() in p['name'].lower() 
            or query.lower() in p.get('description', '').lower()
        ]
    else:
        products = []
    
    return render(request, 'main/search_results.html', {
        'products': products,
        'query': query
    })

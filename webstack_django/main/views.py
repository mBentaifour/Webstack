from django.shortcuts import render
from django.db.models import Q
from .models import Product

# Create your views here.

def home(request):
    search_query = request.GET.get('q', '')
    category = request.GET.get('category', 'all')
    
    products = Product.objects.all()
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category and category != 'all':
        products = products.filter(category=category)
    
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
        'title': 'Accueil'
    }
    
    return render(request, 'main/home.html', context)

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'main/product_detail.html', {
        'product': product,
        'title': product.name
    })

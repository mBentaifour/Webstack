from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Review
from .forms import ReviewForm

# Create your views here.

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'main/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.all().order_by('-created_at')
    review_form = ReviewForm()
    return render(request, 'main/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products
    })

@login_required
def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Votre avis a été ajouté avec succès!')
            return redirect('product_detail', slug=product.slug)
    
    return redirect('product_detail', slug=product.slug)

def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        ).distinct()
    else:
        products = []
    
    return render(request, 'main/search_results.html', {
        'products': products,
        'query': query
    })

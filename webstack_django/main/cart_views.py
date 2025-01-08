from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .supabase_adapter import SupabaseAdapter
import json
from django.contrib import messages

@login_required
def cart_view(request):
    """Vue pour afficher le panier"""
    db = SupabaseAdapter()
    cart = db.get_user_cart(request.user.id)
    return render(request, 'main/cart/cart.html', {'cart': cart})

@login_required
@require_POST
def add_to_cart(request, product_id):
    """Ajouter un produit au panier"""
    db = SupabaseAdapter()
    quantity = int(request.POST.get('quantity', 1))
    
    result = db.add_to_cart(request.user.id, product_id, quantity)
    
    if result.get('success'):
        return JsonResponse({
            'success': True,
            'message': 'Produit ajouté au panier'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de l\'ajout au panier'
        })

@login_required
@require_POST
def update_cart(request, product_id):
    """Mettre à jour la quantité d'un produit dans le panier"""
    db = SupabaseAdapter()
    data = json.loads(request.body)
    action = data.get('action')
    
    if action == 'increase':
        result = db.update_cart_item(request.user.id, product_id, 1)
    elif action == 'decrease':
        result = db.update_cart_item(request.user.id, product_id, -1)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Action non valide'
        })
    
    if result.get('success'):
        return JsonResponse({
            'success': True,
            'message': 'Panier mis à jour'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de la mise à jour du panier'
        })

@login_required
@require_POST
def remove_from_cart(request, product_id):
    """Supprimer un produit du panier"""
    db = SupabaseAdapter()
    result = db.remove_from_cart(request.user.id, product_id)
    
    if result.get('success'):
        return JsonResponse({
            'success': True,
            'message': 'Produit supprimé du panier'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de la suppression du produit'
        })

@login_required
def checkout(request):
    """Vue pour le processus de paiement"""
    db = SupabaseAdapter()
    
    if request.method == 'POST':
        # Récupérer le panier de l'utilisateur
        cart = db.get_user_cart(request.user.id)
        if not cart.get('success') or not cart.get('data', {}).get('items'):
            messages.error(request, 'Votre panier est vide')
            return redirect('main:cart')
        
        # Convertir les items du panier en items de commande
        order_items = [{
            'product_id': item['product']['id'],
            'quantity': item['quantity']
        } for item in cart['data']['items']]
        
        # Créer la commande
        result = db.create_order(request.user.id, order_items)
        
        if result.get('success'):
            # Vider le panier après la commande réussie
            db.clear_cart(request.user.id)
            messages.success(request, 'Votre commande a été créée avec succès')
            return redirect('main:order_detail', order_id=result['data']['order']['id'])
        else:
            messages.error(request, result.get('error', 'Une erreur est survenue lors de la création de la commande'))
            return redirect('main:cart')
    
    # GET request : afficher la page de checkout
    cart = db.get_user_cart(request.user.id)
    user_profile = db.get_user(request.user.id)
    
    context = {
        'cart': cart.get('data', {}),
        'profile': user_profile.get('data', {})
    }
    return render(request, 'main/cart/checkout.html', context)

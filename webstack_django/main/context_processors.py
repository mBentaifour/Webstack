from .supabase_adapter import SupabaseAdapter

def navigation(request):
    """
    Context processor pour ajouter les données de navigation à tous les templates
    """
    db = SupabaseAdapter()
    
    # Récupérer les catégories pour le menu
    categories_data = db.get_categories_with_count()
    categories = categories_data.get('data', []) if categories_data.get('success') else []
    
    # Filtrer les catégories qui n'ont pas de slug
    categories = [cat for cat in categories if cat.get('slug')]
    
    # Récupérer les notifications si l'utilisateur est connecté
    notifications = []
    notifications_count = 0
    if request.user.is_authenticated:
        notifications = db.get_user_notifications(request.user.id)
        notifications_count = len([n for n in notifications if not n.get('read', False)])
    
    # Récupérer le panier si l'utilisateur est connecté
    cart = None
    if request.user.is_authenticated:
        cart = db.get_user_cart(request.user.id)
    
    # Construire le fil d'Ariane
    breadcrumb = []
    current_url = request.path_info.strip('/')
    if current_url:
        parts = current_url.split('/')
        accumulated_url = ''
        for part in parts:
            accumulated_url = f"{accumulated_url}/{part}".strip('/')
            # Vous devrez adapter cette logique selon vos besoins
            title = part.replace('-', ' ').title()
            breadcrumb.append({
                'url': f"/{accumulated_url}",
                'title': title
            })
    
    return {
        'nav_categories': categories,
        'notifications': notifications,
        'notifications_count': notifications_count,
        'cart': cart,
        'breadcrumb': breadcrumb
    }

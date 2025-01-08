from main.supabase_adapter import SupabaseAdapter
from dotenv import load_dotenv
import os

load_dotenv()

def test_order_creation():
    """Test la création d'une commande"""
    db = SupabaseAdapter()
    
    # Se connecter en tant qu'admin
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    
    login_result = db.sign_in(admin_email, admin_password)
    if not login_result.get('success'):
        print(f"[!!] Erreur de connexion: {login_result.get('error')}")
        return
    
    print("[OK] Connecté en tant qu'admin")
    
    # Créer un produit de test si nécessaire
    test_product = {
        'name': 'Produit Test',
        'description': 'Un produit pour tester les commandes',
        'price': 19.99,
        'stock': 10,
        'category_id': None,  # À remplacer par un ID valide
        'brand_id': None,     # À remplacer par un ID valide
        'is_active': True
    }
    
    # Récupérer une catégorie et une marque existantes
    categories = db.get_categories()
    brands = db.get_brands()
    
    if categories.get('success') and categories['data']:
        test_product['category_id'] = categories['data'][0]['id']
    
    if brands.get('success') and brands['data']:
        test_product['brand_id'] = brands['data'][0]['id']
    
    product_result = db.create_product(test_product)
    
    if not product_result.get('success'):
        print(f"[!!] Erreur lors de la création du produit test: {product_result.get('error')}")
        return
    
    print(f"[OK] Produit test créé avec l'ID: {product_result['data']['id']}")
    
    # Créer une commande test
    test_order_items = [{
        'product_id': product_result['data']['id'],
        'quantity': 2
    }]
    
    # ID utilisateur de test (à remplacer par un ID valide)
    test_user_id = os.getenv('TEST_USER_ID')
    
    if not test_user_id:
        print("[!!] TEST_USER_ID non défini dans le fichier .env")
        return
    
    print("\n>>> Test de création de commande...")
    
    # Créer la commande
    order_result = db.create_order(test_user_id, test_order_items)
    
    if order_result.get('success'):
        print(f"[OK] Commande créée avec succès")
        print(f"ID de la commande: {order_result['data']['order']['id']}")
        print(f"Montant total: {order_result['data']['order']['total_amount']} €")
        
        # Vérifier que la commande est récupérable
        print("\n>>> Test de récupération de la commande...")
        order_details = db.get_order_details(order_result['data']['order']['id'], test_user_id)
        
        if order_details.get('success'):
            print("[OK] Détails de la commande récupérés")
            print(f"Statut: {order_details['data']['status']}")
            print(f"Nombre d'articles: {len(order_details['data']['order_items'])}")
        else:
            print(f"[!!] Erreur lors de la récupération des détails: {order_details.get('error')}")
        
        # Tester la mise à jour du statut
        print("\n>>> Test de mise à jour du statut...")
        update_result = db.update_order_status(
            order_result['data']['order']['id'],
            test_user_id,
            'processing'
        )
        
        if update_result.get('success'):
            print("[OK] Statut mis à jour avec succès")
        else:
            print(f"[!!] Erreur lors de la mise à jour du statut: {update_result.get('error')}")
        
    else:
        print(f"[!!] Erreur lors de la création de la commande: {order_result.get('error')}")
    
    print("\n>>> Test terminé!")

if __name__ == "__main__":
    test_order_creation()

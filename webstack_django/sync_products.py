import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
from datetime import datetime

def connect_to_supabase():
    """Établit la connexion à Supabase."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_ANON_KEY')
    return create_client(url, key)

def fetch_products():
    """Récupère tous les produits depuis Supabase."""
    try:
        supabase = connect_to_supabase()
        response = supabase.table('products').select("*").execute()
        return response.data
    except Exception as e:
        print(f"[ERREUR] Récupération des produits: {str(e)}")
        return None

def save_products_to_json(products):
    """Sauvegarde les produits dans un fichier JSON."""
    if not products:
        return False
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'products_backup_{timestamp}.json'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"[OK] Produits sauvegardés dans {filename}")
        return True
    except Exception as e:
        print(f"[ERREUR] Sauvegarde des produits: {str(e)}")
        return False

def display_products(products):
    """Affiche les produits de manière formatée."""
    if not products:
        print("Aucun produit trouvé")
        return

    print(f"\nNombre total de produits: {len(products)}")
    print("\n=== Liste des produits ===")
    for product in products:
        print(f"\nID: {product.get('id')}")
        print(f"Nom: {product.get('name')}")
        print(f"Prix: {product.get('price')}€")
        print(f"Stock: {product.get('stock')}")
        print(f"Catégorie: {product.get('category')}")
        print("-" * 30)

if __name__ == "__main__":
    load_dotenv('.env.new')
    print("\n=== Synchronisation des produits avec Supabase ===")
    
    # Récupération des produits
    products = fetch_products()
    
    if products:
        # Affichage des produits
        display_products(products)
        
        # Sauvegarde dans un fichier JSON
        save_products_to_json(products)
        
        print("\n[OK] Synchronisation terminée avec succès!")
    else:
        print("\n[ERREUR] La synchronisation a échoué.")

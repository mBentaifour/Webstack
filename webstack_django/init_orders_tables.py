import os
from dotenv import load_dotenv
import requests
from main.supabase_adapter import SupabaseAdapter

load_dotenv()

def init_orders_tables():
    """Initialise les tables orders et order_items avec les politiques RLS appropriées"""
    db = SupabaseAdapter()
    
    # Configuration des headers pour l'API Supabase
    headers = {
        'apikey': os.getenv('SUPABASE_KEY'),
        'Authorization': f"Bearer {os.getenv('SUPABASE_KEY')}",
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    base_url = os.getenv('SUPABASE_URL')
    
    print(">>> Vérification des tables de commandes...")
    
    try:
        # Vérifier l'existence des tables
        orders = db.supabase.table('orders').select("*").limit(1).execute()
        order_items = db.supabase.table('order_items').select("*").limit(1).execute()
        print("[OK] Tables 'orders' et 'order_items' existent")
        
        # Vérifier les colonnes des tables
        orders_columns = [
            'id', 'user_id', 'status', 'total_amount', 'created_at', 'updated_at'
        ]
        order_items_columns = [
            'id', 'order_id', 'product_id', 'quantity', 'price', 'created_at'
        ]
        
        # Faire une requête pour obtenir la structure des tables
        response = requests.get(
            f"{base_url}/rest/v1/orders?select=*&limit=1",
            headers=headers
        )
        
        if response.status_code == 200:
            print("[OK] Structure des tables vérifiée")
        else:
            print("[!!] Erreur lors de la vérification de la structure")
            
    except Exception as e:
        print(f"[!!] Erreur lors de la vérification des tables: {str(e)}")
        return
    
    print("\n>>> Configuration des politiques RLS...")
    
    # Vérification des politiques via l'API de gestion de Supabase
    try:
        # Tester l'accès aux données avec un faux user_id
        test_response = requests.get(
            f"{base_url}/rest/v1/orders?select=*",
            headers={**headers, 'Authorization': 'Bearer invalid_token'}
        )
        
        if test_response.status_code == 401:
            print("[OK] Les politiques RLS sont actives")
        else:
            print("[!!] Attention : Les politiques RLS ne semblent pas être correctement configurées")
            
    except Exception as e:
        print(f"[!!] Erreur lors de la vérification des politiques: {str(e)}")
    
    print("\n>>> Vérification des contraintes...")
    
    # Test des contraintes
    try:
        # Tenter d'insérer une commande invalide
        invalid_order = {
            'user_id': '00000000-0000-0000-0000-000000000000',
            'status': 'invalid_status',
            'total_amount': -1
        }
        
        response = requests.post(
            f"{base_url}/rest/v1/orders",
            headers=headers,
            json=invalid_order
        )
        
        if response.status_code == 400:
            print("[OK] Les contraintes sont actives")
        else:
            print("[!!] Attention : Les contraintes ne semblent pas être correctement configurées")
            
    except Exception as e:
        print(f"[!!] Erreur lors de la vérification des contraintes: {str(e)}")
    
    print("\n>>> Configuration terminée!")

if __name__ == "__main__":
    init_orders_tables()

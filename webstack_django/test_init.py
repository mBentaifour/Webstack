from main.supabase_adapter import SupabaseAdapter
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialisation de l'adaptateur Supabase
        db = SupabaseAdapter()
        
        # Initialisation des tables
        result = db.init_tables()
        
        if result.get('success'):
            print("[OK] Tables initialisées avec succès")
            
            # Test de récupération des données
            categories = db.get_categories()
            print(f"\nCatégories ({len(categories)}):")
            for cat in categories:
                if isinstance(cat, dict):
                    print(f"- {cat.get('name', 'N/A')}")
                else:
                    print(f"- {cat}")
            
            brands = db.get_brands()
            print(f"\nMarques ({len(brands)}):")
            for brand in brands:
                if isinstance(brand, dict):
                    print(f"- {brand.get('name', 'N/A')}")
                else:
                    print(f"- {brand}")
            
            products = db.get_products()
            print(f"\nProduits ({len(products)}):")
            for prod in products:
                if isinstance(prod, dict):
                    print(f"- {prod.get('name', 'N/A')} ({prod.get('price', 'N/A')}€)")
                else:
                    print(f"- {prod}")
        else:
            print(f"[ERREUR] {result.get('error')}")
    
    except Exception as e:
        print(f"[ERREUR] {str(e)}")

if __name__ == "__main__":
    main()

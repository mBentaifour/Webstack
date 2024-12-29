from main.supabase_adapter import SupabaseAdapter
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurer le logging
logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Créer une instance de SupabaseAdapter
        db = SupabaseAdapter()
        
        # Tester la connexion
        connection_test = db.test_connection()
        if connection_test:
            print("[OK] Connexion à Supabase établie avec succès\n")
        else:
            print("[ERREUR] Échec de la connexion à Supabase\n")
            return
        
        # Récupérer et afficher les catégories
        categories = db.get_categories()
        print(f"Catégories ({len(categories)}):")
        print("Format des données:", type(categories))
        if categories:
            print("Premier élément:", categories[0])
        print()
        
        # Récupérer et afficher les marques
        brands = db.get_brands()
        print(f"Marques ({len(brands)}):")
        print("Format des données:", type(brands))
        if brands:
            print("Premier élément:", brands[0])
        print()
        
        # Récupérer et afficher les produits
        products = db.get_products()
        print(f"Produits ({len(products)}):")
        print("Format des données:", type(products))
        if products:
            print("Premier élément:", products[0])
        print()
        
    except Exception as e:
        print(f"[ERREUR] {str(e)}")

if __name__ == "__main__":
    main()

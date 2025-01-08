from dotenv import load_dotenv
import os
from supabase import create_client, Client

def add_test_products():
    # Charger les variables d'environnement
    load_dotenv()
    
    # Connexion à Supabase
    supabase: Client = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    try:
        # Se connecter en tant qu'administrateur
        auth_response = supabase.auth.sign_in_with_password({
            "email": "bentaifourmoh@gmail.com",
            "password": "AdminDroguerie2024!"
        })
        
        print("Connexion réussie!")
        
        # Récupérer les IDs des catégories et marques
        categories = supabase.table('categories').select('*').execute()
        brands = supabase.table('brands').select('*').execute()
        
        # Créer un mapping pour faciliter l'accès aux IDs
        category_map = {cat['slug']: cat['id'] for cat in categories.data}
        brand_map = {brand['slug']: brand['id'] for brand in brands.data}
        
        # Produits de test
        products = [
            {
                "name": "Marteau de charpentier Stanley",
                "slug": "marteau-stanley",
                "description": "Marteau robuste avec manche en bois",
                "price": 29.99,
                "stock": 50,
                "category_id": category_map['outillage-a-main'],
                "brand_id": brand_map['stanley'],
                "image_url": "https://example.com/images/marteau-stanley.jpg",
                "is_active": True
            },
            {
                "name": "Perceuse-visseuse Bosch GSR 18V",
                "slug": "perceuse-bosch-gsr18v",
                "description": "Perceuse sans fil 18V avec 2 batteries",
                "price": 199.99,
                "stock": 25,
                "category_id": category_map['electroportatif'],
                "brand_id": brand_map['bosch'],
                "image_url": "https://example.com/images/perceuse-bosch.jpg",
                "is_active": True
            },
            {
                "name": "Jeu de tournevis Facom",
                "slug": "tournevis-facom-set",
                "description": "Set de 6 tournevis professionnels",
                "price": 49.99,
                "stock": 35,
                "category_id": category_map['outillage-a-main'],
                "brand_id": brand_map['facom'],
                "image_url": "https://example.com/images/tournevis-facom.jpg",
                "is_active": True
            }
        ]
        
        # Ajouter les produits
        print("\nAjout des produits...")
        for product in products:
            try:
                response = supabase.table('products').insert(product).execute()
                print(f"Produit ajouté: {product['name']}")
            except Exception as e:
                if "duplicate key" in str(e):
                    print(f"Le produit {product['name']} existe déjà")
                else:
                    print(f"Erreur lors de l'ajout du produit {product['name']}: {str(e)}")
        
        print("\nAjout des produits terminé!")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    add_test_products()

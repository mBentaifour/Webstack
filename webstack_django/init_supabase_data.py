import os
from supabase import create_client
import uuid
from datetime import datetime

# Configuration Supabase
SUPABASE_URL = "https://hbqpplveyaofcqtuippl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhicXBwbHZleWFvZmNxdHVpcHBsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDI3OTU3OSwiZXhwIjoyMDQ5ODU1NTc5fQ.rLdOBtD3uJsEKnbj2QyvoyQVzh0XbsBGN4gITOXq48Y"

def create_test_data():
    if not SUPABASE_KEY:
        print("Erreur: Veuillez ajouter votre cle service_role dans le script")
        return
        
    try:
        # Initialiser le client Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("Connexion a Supabase etablie...")
        
        # Creation des categories
        categories_data = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Outillage a main',
                'slug': 'outillage-a-main',
                'description': 'Outils manuels pour tous vos travaux',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Electroportatif',
                'slug': 'electroportatif',
                'description': 'Outils electriques pour professionnels et particuliers',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Quincaillerie',
                'slug': 'quincaillerie',
                'description': 'Vis, clous, chevilles et autres accessoires',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]

        # Inserer les categories
        print("\nCreation des categories...")
        for category in categories_data:
            try:
                result = supabase.table('categories').insert(category).execute()
                print("[OK] Categorie cree :", category['name'])
            except Exception as e:
                print("[X] Erreur lors de la creation de la categorie", category['name'], ":", str(e))

        # Creation des marques
        brands_data = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Stanley',
                'slug': 'stanley',
                'description': 'Marque leader dans l\'outillage',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Bosch',
                'slug': 'bosch',
                'description': 'Expert en outillage electroportatif',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Facom',
                'slug': 'facom',
                'description': 'Outillage professionnel de qualite',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]

        # Inserer les marques
        print("\nCreation des marques...")
        for brand in brands_data:
            try:
                result = supabase.table('brands').insert(brand).execute()
                print("[OK] Marque cree :", brand['name'])
            except Exception as e:
                print("[X] Erreur lors de la creation de la marque", brand['name'], ":", str(e))

        # Creation des produits
        products_data = [
            {
                'id': str(uuid.uuid4()),
                'name': 'Marteau Stanley',
                'slug': 'marteau-stanley',
                'description': 'Marteau de qualite professionnelle',
                'price': 29.99,
                'stock': 50,
                'category_id': categories_data[0]['id'],
                'brand_id': brands_data[0]['id'],
                'image_url': 'https://example.com/marteau.jpg',
                'is_active': True,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Perceuse Bosch',
                'slug': 'perceuse-bosch',
                'description': 'Perceuse sans fil 18V',
                'price': 199.99,
                'stock': 30,
                'category_id': categories_data[1]['id'],
                'brand_id': brands_data[1]['id'],
                'image_url': 'https://example.com/perceuse.jpg',
                'is_active': True,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Cle a molette Facom',
                'slug': 'cle-a-molette-facom',
                'description': 'Cle a molette professionnelle',
                'price': 45.99,
                'stock': 40,
                'category_id': categories_data[0]['id'],
                'brand_id': brands_data[2]['id'],
                'image_url': 'https://example.com/cle.jpg',
                'is_active': True,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        ]

        # Inserer les produits
        print("\nCreation des produits...")
        for product in products_data:
            try:
                result = supabase.table('products').insert(product).execute()
                print("[OK] Produit cree :", product['name'])
            except Exception as e:
                print("[X] Erreur lors de la creation du produit", product['name'], ":", str(e))

        print("\nInitialisation terminee avec succes!")
        
    except Exception as e:
        print(f"Erreur generale : {str(e)}")

if __name__ == '__main__':
    print("Initialisation des donnees de test dans Supabase...")
    create_test_data()
    print("\nTermine!")

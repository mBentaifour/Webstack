from supabase import create_client, Client

# Configuration Supabase
SUPABASE_URL = "https://hbqpplveyaofcqtuippl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhicXBwbHZleWFvZmNxdHVpcHBsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyNzk1NzksImV4cCI6MjA0OTg1NTU3OX0.g-JyzBu2A8-_dm56lSxjGOHJ8FLN7cB7TbebxWvVjmA"

def add_test_data():
    # Connexion à Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        # Se connecter avec le compte admin
        auth_response = supabase.auth.sign_in_with_password({
            "email": "bentaifourmoh@gmail.com",
            "password": "AdminDroguerie2024!"
        })
        
        print("Connexion réussie!")
        
        # Ajouter les catégories
        print("\nAjout des catégories...")
        categories = [
            {"name": "Outillage à main", "slug": "outillage-main", "description": "Outils manuels pour tous vos travaux"},
            {"name": "Électroportatif", "slug": "electroportatif", "description": "Outils électriques professionnels"},
            {"name": "Quincaillerie", "slug": "quincaillerie", "description": "Visserie et accessoires"},
            {"name": "Peinture", "slug": "peinture", "description": "Peintures et accessoires"},
            {"name": "Jardinage", "slug": "jardinage", "description": "Outils de jardinage"}
        ]
        
        for category in categories:
            try:
                result = supabase.table('categories').insert(category).execute()
                print(f"✓ Catégorie ajoutée : {category['name']}")
            except Exception as e:
                if "duplicate key" in str(e):
                    print(f"! Catégorie déjà existante : {category['name']}")
                else:
                    print(f"✗ Erreur lors de l'ajout de {category['name']}: {str(e)}")
        
        # Ajouter les marques
        print("\nAjout des marques...")
        brands = [
            {"name": "Stanley", "slug": "stanley", "description": "Outillage professionnel"},
            {"name": "Bosch", "slug": "bosch", "description": "Leader de l'électroportatif"},
            {"name": "Facom", "slug": "facom", "description": "Outillage de qualité"},
            {"name": "Makita", "slug": "makita", "description": "Outils électroportatifs professionnels"},
            {"name": "DeWalt", "slug": "dewalt", "description": "Outillage électroportatif professionnel"}
        ]
        
        for brand in brands:
            try:
                result = supabase.table('brands').insert(brand).execute()
                print(f"✓ Marque ajoutée : {brand['name']}")
            except Exception as e:
                if "duplicate key" in str(e):
                    print(f"! Marque déjà existante : {brand['name']}")
                else:
                    print(f"✗ Erreur lors de l'ajout de {brand['name']}: {str(e)}")
        
        # Ajouter quelques produits de test
        print("\nAjout des produits de test...")
        products = [
            {
                "name": "Marteau Stanley",
                "slug": "marteau-stanley",
                "description": "Marteau de qualité professionnelle",
                "price": 29.99,
                "stock": 50,
                "image_url": "https://example.com/marteau.jpg",
                "is_active": True
            },
            {
                "name": "Perceuse Bosch",
                "slug": "perceuse-bosch",
                "description": "Perceuse sans fil 18V",
                "price": 199.99,
                "stock": 25,
                "image_url": "https://example.com/perceuse.jpg",
                "is_active": True
            },
            {
                "name": "Clé à molette Facom",
                "slug": "cle-molette-facom",
                "description": "Clé à molette professionnelle",
                "price": 45.99,
                "stock": 30,
                "image_url": "https://example.com/cle.jpg",
                "is_active": True
            }
        ]
        
        # Récupérer les IDs des catégories et marques
        cats = supabase.table('categories').select('id, name').execute()
        brands_data = supabase.table('brands').select('id, name').execute()
        
        categories_dict = {cat['name']: cat['id'] for cat in cats.data}
        brands_dict = {brand['name']: brand['id'] for brand in brands_data.data}
        
        # Associer les produits aux catégories et marques
        products[0].update({
            "category_id": categories_dict.get("Outillage à main"),
            "brand_id": brands_dict.get("Stanley")
        })
        
        products[1].update({
            "category_id": categories_dict.get("Électroportatif"),
            "brand_id": brands_dict.get("Bosch")
        })
        
        products[2].update({
            "category_id": categories_dict.get("Outillage à main"),
            "brand_id": brands_dict.get("Facom")
        })
        
        for product in products:
            try:
                result = supabase.table('products').insert(product).execute()
                print(f"✓ Produit ajouté : {product['name']}")
            except Exception as e:
                if "duplicate key" in str(e):
                    print(f"! Produit déjà existant : {product['name']}")
                else:
                    print(f"✗ Erreur lors de l'ajout de {product['name']}: {str(e)}")
        
        print("\nConfiguration des données de test terminée!")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    add_test_data()

from dotenv import load_dotenv
import os
from supabase import create_client, Client

def setup_initial_data():
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
        
        # Catégories
        categories = [
            {
                "name": "Outillage à main",
                "slug": "outillage-a-main",
                "description": "Outils manuels pour vos travaux"
            },
            {
                "name": "Électroportatif",
                "slug": "electroportatif",
                "description": "Outils électriques pour professionnels et particuliers"
            },
            {
                "name": "Quincaillerie",
                "slug": "quincaillerie",
                "description": "Visserie, boulonnerie et accessoires"
            }
        ]
        
        # Marques
        brands = [
            {
                "name": "Bosch",
                "slug": "bosch",
                "description": "Leader mondial des outils électroportatifs"
            },
            {
                "name": "Stanley",
                "slug": "stanley",
                "description": "Spécialiste de l'outillage à main"
            },
            {
                "name": "Facom",
                "slug": "facom",
                "description": "Outillage professionnel de haute qualité"
            }
        ]
        
        # Ajouter les catégories
        print("\nAjout des catégories...")
        for category in categories:
            try:
                response = supabase.table('categories').insert(category).execute()
                print(f"Catégorie ajoutée: {category['name']}")
            except Exception as e:
                if "duplicate key" in str(e):
                    print(f"La catégorie {category['name']} existe déjà")
                else:
                    print(f"Erreur lors de l'ajout de la catégorie {category['name']}: {str(e)}")
        
        # Ajouter les marques
        print("\nAjout des marques...")
        for brand in brands:
            try:
                response = supabase.table('brands').insert(brand).execute()
                print(f"Marque ajoutée: {brand['name']}")
            except Exception as e:
                if "duplicate key" in str(e):
                    print(f"La marque {brand['name']} existe déjà")
                else:
                    print(f"Erreur lors de l'ajout de la marque {brand['name']}: {str(e)}")
        
        print("\nConfiguration initiale terminée!")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    setup_initial_data()

from dotenv import load_dotenv
import os
from supabase import create_client

def test_connection():
    try:
        # Charger les variables d'environnement
        load_dotenv()
        
        # Récupérer les informations de connexion
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        print("URL Supabase:", supabase_url)
        print("Clé Supabase trouvée:", bool(supabase_key))
        
        # Créer le client Supabase
        supabase = create_client(supabase_url, supabase_key)
        
        # Tester une requête simple
        response = supabase.table('products').select("*").limit(1).execute()
        
        print("\nConnexion réussie!")
        print("Nombre de produits trouvés:", len(response.data))
        if response.data:
            print("Premier produit:", response.data[0])
            
    except Exception as e:
        print(f"Erreur lors de la connexion: {str(e)}")

if __name__ == "__main__":
    test_connection()

from supabase_config import get_supabase_client
import os
from dotenv import load_dotenv

def test_supabase_connection():
    try:
        # Charger les variables d'environnement
        load_dotenv()
        
        # Vérifier si les variables sont présentes
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("Erreur: SUPABASE_URL ou SUPABASE_KEY non trouvé dans le fichier .env")
            return False
            
        print("URL Supabase:", supabase_url)
        print("Clé trouvée:", "Oui" if supabase_key else "Non")
        
        # Tester la connexion
        supabase = get_supabase_client()
        
        # Tester une requête simple
        response = supabase.table('products').select("*").limit(1).execute()
        print("\nConnexion à Supabase réussie!")
        print("Données reçues:", response.data)
        return True
        
    except Exception as e:
        print("\nErreur de connexion à Supabase:", str(e))
        return False

if __name__ == "__main__":
    test_supabase_connection()

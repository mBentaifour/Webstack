from django.conf import settings
from supabase import create_client, Client

def get_supabase_client() -> Client:
    """
    Crée et retourne un client Supabase configuré
    """
    return create_client(
        settings.SUPABASE['URL'],
        settings.SUPABASE['ANON_KEY']
    )

def test_connection():
    """
    Teste la connexion à Supabase
    """
    try:
        client = get_supabase_client()
        
        # Test de la connexion en récupérant les données d'une table
        response = client.table('produits').select("*").limit(1).execute()
        print("Connexion réussie !")
        print(f"Données récupérées : {response.data}")
        return True
    except Exception as e:
        print(f"Erreur de connexion : {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()

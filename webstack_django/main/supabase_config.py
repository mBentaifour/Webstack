from dotenv import load_dotenv
import os
from supabase import create_client, Client
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    """Crée et retourne un client Supabase."""
    try:
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("Les variables d'environnement SUPABASE_URL et SUPABASE_KEY sont requises")
            
        client = create_client(supabase_url, supabase_key)
        logger.info("Client Supabase créé avec succès")
        return client
        
    except Exception as e:
        logger.error(f"Erreur lors de la création du client Supabase: {str(e)}")
        raise

def get_supabase_admin_client() -> Client:
    """Crée et retourne un client Supabase avec les droits d'administration."""
    try:
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not supabase_url or not service_key:
            raise ValueError("Les variables d'environnement SUPABASE_URL et SUPABASE_SERVICE_KEY sont requises")
            
        client = create_client(supabase_url, service_key)
        logger.info("Client Supabase admin créé avec succès")
        return client
        
    except Exception as e:
        logger.error(f"Erreur lors de la création du client Supabase admin: {str(e)}")
        raise

def test_supabase_connection():
    """Teste la connexion à Supabase."""
    try:
        client = get_supabase_client()
        # Test simple : récupérer une catégorie
        response = client.table('categories').select('id').limit(1).execute()
        logger.info("Test de connexion Supabase réussi")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du test de connexion Supabase: {str(e)}")
        return False

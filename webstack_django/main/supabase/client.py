from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Instance unique du client Supabase
_supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    """
    Retourne une instance unique du client Supabase.
    Utilise le pattern Singleton pour éviter de créer plusieurs connexions.
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            load_dotenv()
            
            url = os.getenv('SUPABASE_URL')
            key = os.getenv('SUPABASE_KEY')
            
            if not url or not key:
                raise ValueError("Les variables d'environnement SUPABASE_URL et SUPABASE_KEY sont requises")
            
            _supabase_client = create_client(url, key)
            logger.info("Client Supabase initialisé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client Supabase: {str(e)}")
            raise
    
    return _supabase_client

def reset_supabase_client():
    """Réinitialise le client Supabase (utile pour les tests)"""
    global _supabase_client
    _supabase_client = None

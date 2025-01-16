import os
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

class SupabaseAuth:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY doivent être définis dans les variables d'environnement")
        
        self.client: Client = create_client(url, key)
        logger.info("Client Supabase créé avec succès")

    def sign_in_with_password(self, email: str, password: str) -> dict:
        """
        Authentifie un utilisateur avec son email et son mot de passe.
        Retourne les données de session si l'authentification réussit.
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response.session
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification: {str(e)}")
            raise

    def verify_token(self, token: str) -> bool:
        """
        Vérifie la validité d'un token d'accès.
        Retourne True si le token est valide, False sinon.
        """
        try:
            # Définir le token dans le client
            self.client.auth.set_session(token, None)
            # Récupérer l'utilisateur actuel (lève une exception si le token est invalide)
            user = self.client.auth.get_user()
            return bool(user)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du token: {str(e)}")
            return False

    def sign_out(self, token: str) -> None:
        """
        Déconnecte l'utilisateur.
        """
        try:
            self.client.auth.set_session(token, None)
            self.client.auth.sign_out()
        except Exception as e:
            logger.error(f"Erreur lors de la déconnexion: {str(e)}")
            raise

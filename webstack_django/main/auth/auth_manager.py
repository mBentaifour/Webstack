import logging
from typing import Dict, Optional
from ..supabase.client import get_supabase_client

logger = logging.getLogger(__name__)

class AuthManager:
    """Gestionnaire d'authentification utilisant Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def sign_up(self, email: str, password: str, user_data: Dict) -> Dict:
        """Inscription d'un nouvel utilisateur"""
        try:
            # Création du compte utilisateur
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_data
                }
            })
            
            if not auth_response.user:
                return {"success": False, "error": "Échec de l'inscription"}
            
            user_dict = {
                "id": auth_response.user.id,
                "email": email,
                **user_data
            }
            
            return {"success": True, "user": user_dict}
            
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def sign_in(self, email: str, password: str) -> Dict:
        """Connexion d'un utilisateur"""
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response and response.user:
                user_dict = {
                    "id": response.user.id,
                    "email": response.user.email,
                    **(response.user.user_metadata or {})
                }
                return {"success": True, "user": user_dict}
            return {"success": False, "error": "Identifiants invalides"}
            
        except Exception as e:
            logger.error(f"Erreur lors de la connexion : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def sign_out(self) -> Dict:
        """Déconnexion de l'utilisateur"""
        try:
            self.supabase.auth.sign_out()
            return {"success": True}
        except Exception as e:
            logger.error(f"Erreur lors de la déconnexion : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def reset_password(self, email: str) -> Dict:
        """Demande de réinitialisation du mot de passe"""
        try:
            self.supabase.auth.reset_password_email(email)
            return {"success": True}
        except Exception as e:
            logger.error(f"Erreur lors de la demande de réinitialisation : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def update_password(self, new_password: str) -> Dict:
        """Mise à jour du mot de passe"""
        try:
            self.supabase.auth.update_user({"password": new_password})
            return {"success": True}
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du mot de passe : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_user(self) -> Optional[Dict]:
        """Récupère l'utilisateur actuellement connecté"""
        try:
            response = self.supabase.auth.get_user()
            if not response or not response.user:
                return None
                
            return {
                "id": response.user.id,
                "email": response.user.email,
                **(response.user.user_metadata or {})
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")
            return None
    
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur actuel est un administrateur"""
        try:
            user = self.get_user()
            if user is None:
                return False
            return user.get("is_admin", False)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du statut admin : {str(e)}")
            return False

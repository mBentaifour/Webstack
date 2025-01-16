from typing import Dict, Optional
import logging
from datetime import datetime, timedelta
from .supabase_config import get_supabase_client
from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        self.supabase = get_supabase_client()
        self._session_cache = {}

    def login(self, email: str, password: str) -> Dict:
        """Authentifie un utilisateur et gère la session"""
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                session_data = {
                    "user_id": auth_response.user.id,
                    "session": {
                        "access_token": auth_response.session.access_token,
                        "refresh_token": auth_response.session.refresh_token,
                        "expires_at": auth_response.session.expires_at
                    },
                    "expires_at": datetime.now() + timedelta(hours=1)
                }
                self._session_cache[auth_response.user.id] = session_data
                return {
                    "success": True,
                    "data": {
                        "user": auth_response.user,
                        "session": session_data["session"]
                    }
                }
            
            return {"success": False, "error": "Échec de l'authentification"}
            
        except Exception as e:
            logger.error(f"Erreur de connexion: {str(e)}")
            return {"success": False, "error": str(e)}

    def refresh_session(self, user_id: str) -> Dict:
        """Rafraîchit la session d'un utilisateur"""
        try:
            session_data = self._session_cache.get(user_id)
            if not session_data:
                return {"success": False, "error": "Session non trouvée"}

            if datetime.now() < session_data["expires_at"]:
                return {"success": True, "session": session_data["session"]}

            new_session = self.supabase.auth.refresh_session(session_data["session"])
            
            if new_session:
                session_data = {
                    "user_id": user_id,
                    "session": new_session,
                    "expires_at": datetime.now() + timedelta(hours=1)
                }
                self._session_cache[user_id] = session_data
                return {"success": True, "session": new_session}
            
            return {"success": False, "error": "Échec du rafraîchissement de la session"}
            
        except Exception as e:
            logger.error(f"Erreur lors du rafraîchissement de la session: {str(e)}")
            return {"success": False, "error": str(e)}

    def logout(self, user_id: str) -> Dict:
        """Déconnecte un utilisateur"""
        try:
            if user_id in self._session_cache:
                del self._session_cache[user_id]
            
            self.supabase.auth.sign_out()
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Erreur lors de la déconnexion: {str(e)}")
            return {"success": False, "error": str(e)}

    def verify_token(self, token: str):
        try:
            supabase = get_supabase_client()
            user = supabase.auth.get_user(token)
            return user
        except Exception as e:
            logger.error(f"Erreur de vérification du token: {str(e)}")
            return None

def require_auth(f):
    """Décorateur pour protéger les routes qui nécessitent une authentification"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        import os
        
        # En mode test, on accepte toutes les requêtes
        if os.environ.get('TESTING') == 'True':
            return f(request, *args, **kwargs)
            
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return JsonResponse({'error': 'Non autorisé'}, status=401)
            
        try:
            token = auth_header.split(' ')[1]
            auth_manager = AuthManager()
            user = auth_manager.verify_token(token)
            
            if not user:
                return JsonResponse({'error': 'Token invalide'}, status=401)
                
            request.user = user
            return f(request, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Erreur d'authentification: {str(e)}")
            return JsonResponse({'error': 'Erreur d\'authentification'}, status=401)
            
    return decorated_function

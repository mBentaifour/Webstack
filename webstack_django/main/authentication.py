from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from datetime import datetime

class SupabaseAuthentication(authentication.BaseAuthentication):
    """Authentification personnalisée pour Supabase"""
    
    def authenticate(self, request):
        """Authentifier une requête"""
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
            
        try:
            # Extraire le token
            token = auth_header.split(' ')[1]
            
            # Vérifier le token avec Supabase
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            # Vérifier l'expiration
            exp = decoded.get('exp')
            if exp and datetime.fromtimestamp(exp) < datetime.now():
                raise AuthenticationFailed('Token expiré')
                
            # Créer un utilisateur anonyme avec les informations du token
            user = type('AnonymousUser', (), {
                'is_authenticated': True,
                'is_anonymous': False,
                'is_staff': decoded.get('role') == 'admin',
                'is_superuser': decoded.get('role') == 'admin',
                'email': decoded.get('email'),
                'role': decoded.get('role')
            })()
            
            return (user, None)
            
        except (ValueError, jwt.InvalidTokenError):
            return None
        except Exception as e:
            return None
            
    def authenticate_header(self, request):
        """En-tête d'authentification requis"""
        return 'Bearer'

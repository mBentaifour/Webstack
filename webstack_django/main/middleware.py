import logging
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.http import JsonResponse
from .supabase_adapter import SupabaseAdapter
from .auth_manager import AuthManager
import time

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Ajouter des en-têtes de sécurité
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'same-origin'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limits = {}

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Nettoyer les anciennes entrées
        self.cleanup_old_entries(current_time)
        
        # Vérifier le rate limit
        if not self.check_rate_limit(client_ip, current_time):
            return JsonResponse({
                'error': 'Trop de requêtes. Veuillez réessayer plus tard.'
            }, status=429)
        
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def check_rate_limit(self, client_ip, current_time):
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = []
        
        # Ajouter la requête actuelle
        self.rate_limits[client_ip].append(current_time)
        
        # Vérifier le nombre de requêtes dans la dernière minute
        recent_requests = [t for t in self.rate_limits[client_ip] 
                         if current_time - t < 60]
        self.rate_limits[client_ip] = recent_requests
        
        return len(recent_requests) <= 60  # 60 requêtes par minute

    def cleanup_old_entries(self, current_time):
        for ip in list(self.rate_limits.keys()):
            self.rate_limits[ip] = [t for t in self.rate_limits[ip] 
                                  if current_time - t < 60]
            if not self.rate_limits[ip]:
                del self.rate_limits[ip]

class SupabaseSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth_manager = AuthManager()

    def __call__(self, request):
        # Liste des URLs qui ne nécessitent pas d'authentification
        public_urls = [
            'main:home',
            'main:product_list',
            'main:product_detail',
            'main:category_list',
            'main:category_detail',
            'main:search',
            'main:login',
            'main:register',
            'main:logout',
            'admin:index',
            'admin:login',
        ]

        # Toujours autoriser l'accès aux fichiers statiques et media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        try:
            # Obtenir le nom de l'URL actuelle
            current_url = resolve(request.path_info)
            current_view = f"{current_url.namespace}:{current_url.url_name}" if current_url.namespace else current_url.url_name

            # Si l'URL est publique ou si c'est une URL admin, on continue normalement
            if current_view in public_urls or request.path.startswith('/admin/'):
                return self.get_response(request)

            # Vérifier le token d'authentification
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'error': 'Non autorisé'}, status=401)
                messages.warning(request, "Veuillez vous connecter pour accéder à cette page.")
                return redirect('main:login')

            try:
                # Vérifier et rafraîchir la session si nécessaire
                token = auth_header.split(' ')[1]
                user = self.auth_manager.supabase.auth.get_user(token)
                
                if not user:
                    raise Exception("Session invalide")
                
                # Rafraîchir la session si nécessaire
                session_result = self.auth_manager.refresh_session(user.id)
                if not session_result['success']:
                    raise Exception("Impossible de rafraîchir la session")
                
                # Ajouter l'utilisateur à la requête
                request.user = user
                
            except Exception as e:
                logger.error(f"Erreur de session: {str(e)}")
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'error': 'Session expirée'}, status=401)
                messages.error(request, "Votre session a expiré. Veuillez vous reconnecter.")
                return redirect('main:login')

        except Exception as e:
            logger.error(f"Erreur middleware: {str(e)}")
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': 'Erreur serveur'}, status=500)
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
            return redirect('main:home')

        return self.get_response(request)

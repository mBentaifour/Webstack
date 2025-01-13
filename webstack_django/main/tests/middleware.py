from django.contrib.auth.models import User
from django.contrib.auth import login
import os

class TestAuthMiddleware:
    """
    Middleware pour simuler l'authentification dans les tests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si nous sommes en mode test
        if os.environ.get('TESTING') == 'True':
            # Récupérer ou créer l'utilisateur de test
            try:
                user = User.objects.get(username='testuser')
            except User.DoesNotExist:
                return self.get_response(request)
                
            # Forcer l'authentification de l'utilisateur
            request.user = user
            request.session['supabase_access_token'] = 'fake_test_token'
            
        return self.get_response(request)

import os
from functools import wraps
from django.contrib.auth.models import User
from main.models import SupabaseUser
from main.supabase_auth import SupabaseAuth
from django.test import Client
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

def with_test_auth(f):
    """
    Décorateur pour les méthodes de test qui nécessitent une authentification.
    Configure automatiquement :
    - Mode test activé
    - Utilisateur de test créé et connecté
    - Session Supabase simulée
    - Mock de la vérification du token
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        # Activation du mode test
        os.environ['TESTING'] = 'True'
        
        # Configuration de Supabase pour les tests
        os.environ['SUPABASE_URL'] = 'https://hbqppveyaofcqtqipp.supabase.co'
        os.environ['SUPABASE_KEY'] = 'test-key'
        
        # Utilisation de l'utilisateur existant
        try:
            user = User.objects.get(username='testuser')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='testuser',
                email='bentaifourmoh@gmail.com',
                password='AdminDroguerie2024!'
            )
            SupabaseUser.objects.create(
                user=user,
                supabase_uid='6742e94f-f8f4-410a-9a5a-6e3f2efb7d55'
            )
        
        # Création d'un nouveau client de test
        self.client = Client()
        
        # Login de l'utilisateur
        logged_in = self.client.login(username='testuser', password='AdminDroguerie2024!')
        if not logged_in:
            raise Exception("Could not log in test user")
        
        # Configuration de la session
        session = self.client.session
        session['supabase_access_token'] = 'fake_test_token'
        session['_auth_user_id'] = str(user.id)
        session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
        session['_auth_user_hash'] = user.get_session_auth_hash()
        session.save()
        
        # Ajout des métadonnées de test à l'environnement
        os.environ['DJANGO_SETTINGS_MODULE'] = 'webstack_django.settings'
        os.environ['TESTING'] = 'True'
        
        # Mock de la vérification du token
        original_verify = getattr(SupabaseAuth, 'verify_token', None)
        SupabaseAuth.verify_token = lambda self, token: True
        
        try:
            # Exécution du test
            result = f(self, *args, **kwargs)
        finally:
            # Nettoyage
            os.environ['TESTING'] = 'False'
            if original_verify:
                SupabaseAuth.verify_token = original_verify
        
        return result
    
    return wrapper

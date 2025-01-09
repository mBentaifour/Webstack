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
            # Simuler l'authentification
            request.META['TESTING'] = True
            request.user.is_authenticated = True
            request.session['supabase_access_token'] = 'fake_test_token'
        return self.get_response(request)

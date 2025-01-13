from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.supabase_auth import SupabaseAuth
import os

def supabase_auth_required(view_func):
    """
    Décorateur pour vérifier l'authentification Supabase.
    Redirige vers la page de connexion si l'utilisateur n'est pas authentifié.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Vérifier si nous sommes en mode test
        if os.environ.get('TESTING') == 'True':
            # En mode test, on vérifie si un token de test est présent dans la session
            if request.session.get('supabase_access_token'):
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('main:login'))
            
        # En mode production, on vérifie le token avec Supabase
        token = request.session.get('supabase_access_token')
        if not token:
            return HttpResponseRedirect(reverse('main:login'))

        # Vérifier la validité du token avec Supabase
        auth = SupabaseAuth()
        try:
            auth.verify_token(token)
            return view_func(request, *args, **kwargs)
        except Exception:
            # Token invalide ou expiré
            if 'supabase_access_token' in request.session:
                del request.session['supabase_access_token']
            return HttpResponseRedirect(reverse('main:login'))

    return _wrapped_view

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from supabase import create_client
import os
from dotenv import load_dotenv
from .utils.db_get_data import email_exists

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

try:
    # Initialiser le client Supabase avec une configuration minimale
    supabase = create_client(supabase_url, supabase_key, {
        'auto_refresh_token': True,
        'persist_session': True
    })
except Exception as e:
    print(f"Erreur lors de l'initialisation de Supabase: {str(e)}")
    supabase = None

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    if not supabase:
        return JsonResponse({'error': 'Supabase client not initialized'}, status=500)
        
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Vérifier si l'email existe déjà
        if email_exists(email):
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        # Créer un nouvel utilisateur
        user = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': user
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def signin(request):
    if not supabase:
        return JsonResponse({'error': 'Supabase client not initialized'}, status=500)
        
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Connecter l'utilisateur
        user = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        return JsonResponse({
            'message': 'Login successful',
            'session': user
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ... existing code ... 
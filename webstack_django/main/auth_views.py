import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from .supabase_adapter import SupabaseAdapter

logger = logging.getLogger(__name__)

def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('main:home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs")
            return render(request, 'main/login.html')
            
        try:
            db = SupabaseAdapter()
            result = db.sign_in(email=email, password=password)
            
            if result.get('success'):
                # Stocker la session Supabase
                request.session['supabase_session'] = result['data']['session']
                
                # Récupérer l'utilisateur Django par email de manière unique
                try:
                    user = User.objects.filter(email=email).first()
                    if not user:
                        # Créer l'utilisateur s'il n'existe pas
                        username = email.split('@')[0]
                        user = User.objects.create_user(
                            username=f"{username}_{result['data']['user']['id'][:8]}",
                            email=email,
                            password=password
                        )
                    
                    django_login(request, user)
                    messages.success(request, "Connexion réussie!")
                    return redirect('main:home')
                    
                except Exception as e:
                    logger.error(f"Erreur lors de la récupération/création de l'utilisateur Django: {str(e)}")
                    messages.error(request, "Erreur lors de la connexion")
            else:
                messages.error(request, result.get('error', "Email ou mot de passe incorrect"))
                
        except Exception as e:
            logger.error(f"Erreur lors de la connexion: {str(e)}")
            messages.error(request, "Une erreur est survenue lors de la connexion")
    
    return render(request, 'main/login.html')

def register_view(request):
    """Vue d'inscription"""
    if request.user.is_authenticated:
        return redirect('main:home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        full_name = request.POST.get('full_name', '')
        
        # Validation des champs
        if not all([username, email, password, password_confirm]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires")
            return render(request, 'main/register.html')
            
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, 'main/register.html')
            
        if len(password) < 6:
            messages.error(request, "Le mot de passe doit contenir au moins 6 caractères")
            return render(request, 'main/register.html')
        
        try:
            # Vérifier si l'email existe déjà dans Supabase
            db = SupabaseAdapter()
            
            # Créer l'utilisateur dans Supabase
            signup_result = db.sign_up(
                email=email,
                password=password,
                options={
                    'data': {
                        'username': username,
                        'full_name': full_name
                    }
                }
            )
            
            if signup_result.get('success'):
                user_data = signup_result['data']
                
                # Créer le profil utilisateur
                profile_data = {
                    'user_id': user_data['id'],
                    'username': username,
                    'full_name': full_name,
                    'email': email
                }
                
                profile_result = db.create_profile(user_data['id'], profile_data)
                
                if not profile_result.get('success'):
                    logger.error(f"Erreur lors de la création du profil: {profile_result.get('error')}")
                    messages.warning(request, "Compte créé mais erreur lors de la création du profil")
                
                # Connecter l'utilisateur
                login_result = db.sign_in(email=email, password=password)
                
                if login_result.get('success'):
                    # Stocker la session Supabase
                    request.session['supabase_session'] = login_result['data']['session']
                    
                    # Créer l'utilisateur Django
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    
                    django_login(request, user)
                    messages.success(request, "Inscription réussie! Bienvenue!")
                    return redirect('main:home')
                else:
                    messages.error(request, "Compte créé mais erreur lors de la connexion automatique")
                    return redirect('main:login')
            else:
                error_msg = signup_result.get('error', "Erreur lors de l'inscription")
                messages.error(request, error_msg)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {str(e)}")
            messages.error(request, "Une erreur est survenue lors de l'inscription")
    
    return render(request, 'main/register.html')

def logout_view(request):
    """Vue de déconnexion"""
    try:
        # Déconnexion de Supabase
        if 'supabase_session' in request.session:
            db = SupabaseAdapter()
            db.sign_out()
            del request.session['supabase_session']
        
        # Déconnexion de Django
        django_logout(request)
        messages.success(request, "Déconnexion réussie!")
    except Exception as e:
        logger.exception("Erreur lors de la déconnexion")
        messages.error(request, f"Une erreur s'est produite: {str(e)}")
    
    return redirect('main:login')

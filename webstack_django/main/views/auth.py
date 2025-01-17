from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'User with this email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )
    
    token = generate_jwt_token(user)
    
    return Response({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise User.DoesNotExist
            
        token = generate_jwt_token(user)
        
        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        })
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm='HS256')

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """
    @api {post} /auth/password-reset/ Demander une réinitialisation de mot de passe
    @apiDescription Envoie un email avec un lien de réinitialisation de mot de passe
    @apiParam {String} email Email de l'utilisateur
    """
    email = request.data.get('email')
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        token = generate_password_reset_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        # Envoyer l'email
        send_password_reset_email(user.email, reset_url)
        
        return Response({'message': 'Password reset email sent'})
    except User.DoesNotExist:
        # Pour des raisons de sécurité, ne pas révéler si l'email existe
        return Response({'message': 'If this email exists, a reset link has been sent'})

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    @api {post} /auth/password-reset/confirm/ Réinitialiser le mot de passe
    @apiParam {String} token Token de réinitialisation
    @apiParam {String} password Nouveau mot de passe
    """
    token = request.data.get('token')
    password = request.data.get('password')
    
    if not token or not password:
        return Response(
            {'error': 'Token and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        
        # Vérifier que le token n'a pas expiré
        if datetime.fromtimestamp(payload['exp']) < datetime.utcnow():
            return Response(
                {'error': 'Token has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(password)
        user.save()
        
        return Response({'message': 'Password successfully reset'})
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """
    @api {post} /auth/verify-email/ Vérifier l'adresse email
    @apiParam {String} token Token de vérification
    """
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'error': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        
        if user.is_active:
            return Response({'message': 'Email already verified'})
        
        user.is_active = True
        user.save()
        
        return Response({'message': 'Email successfully verified'})
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )

def send_password_reset_email(email, reset_url):
    """Envoie l'email de réinitialisation de mot de passe"""
    subject = 'Réinitialisation de votre mot de passe'
    from_email = settings.DEFAULT_FROM_EMAIL
    html_message = render_to_string('emails/password_reset.html', {
        'reset_url': reset_url
    })
    send_mail(
        subject,
        strip_tags(html_message),
        from_email,
        [email],
        html_message=html_message
    )

def generate_password_reset_token(user):
    """Génère un token JWT pour la réinitialisation de mot de passe"""
    payload = {
        'user_id': user.id,
        'type': 'password_reset',
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

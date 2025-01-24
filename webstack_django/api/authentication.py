from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from supabase import create_client, Client

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the request header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        if not token:
            return None

        try:
            # Initialize Supabase client
            supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            
            # Verify the token and get user data
            user_data = supabase.auth.get_user(token)
            
            if not user_data:
                raise exceptions.AuthenticationFailed('Invalid token')

            # Get or create Django user
            user, created = User.objects.get_or_create(
                username=user_data.user.email,
                defaults={
                    'email': user_data.user.email,
                    'is_active': True
                }
            )

            return (user, token)

        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid token')

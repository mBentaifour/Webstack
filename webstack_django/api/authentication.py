from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from supabase import create_client

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        # Extract the token
        token = auth_header.split(' ')[1]

        try:
            # Initialize Supabase client
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            
            # Verify the token and get user data
            user = supabase.auth.get_user(token)
            
            if not user or not user.user:
                raise AuthenticationFailed('Invalid token')
            
            return (user.user, None)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

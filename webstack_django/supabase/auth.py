from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .client import get_supabase_client

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            supabase = get_supabase_client()
            user = supabase.auth.get_user(token)
            return (user, None)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

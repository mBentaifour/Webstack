from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Extract the token
            token = auth_header.split(' ')[1]
            # Decode the token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            
            # Verify token expiration
            exp = datetime.fromtimestamp(payload['exp'])
            if datetime.now() > exp:
                raise AuthenticationFailed('Token expired')
            
            # Verify token not before time
            if 'nbf' in payload:
                nbf = datetime.fromtimestamp(payload['nbf'])
                if datetime.now() < nbf:
                    raise AuthenticationFailed('Token not yet valid')
            
            # Additional custom claims verification can be added here
            if 'roles' not in payload:
                raise AuthenticationFailed('Invalid token: missing roles')
            
            return (payload, None)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

def generate_token(user_id, roles, expires_in=3600):
    """Generate a JWT token for a user
    
    Args:
        user_id: The user's ID
        roles: List of role names
        expires_in: Token validity in seconds (default 1 hour)
    """
    now = datetime.utcnow()
    payload = {
        'user_id': user_id,
        'roles': roles,
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(seconds=expires_in),
        'iss': 'webstack',  # Token issuer
        'aud': 'webstack-api'  # Intended audience
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

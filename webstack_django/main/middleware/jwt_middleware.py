import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._should_check_jwt(request.path):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'No authorization token provided'}, status=401)

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=['HS256'])
            request.user_id = payload.get('sub')
            request.user_role = payload.get('role', 'user')
        except (jwt.InvalidTokenError, IndexError) as e:
            logger.error(f"JWT validation failed: {str(e)}")
            return JsonResponse({'error': 'Invalid authorization token'}, status=401)
        except Exception as e:
            logger.error(f"Unexpected error in JWT middleware: {str(e)}")
            return JsonResponse({'error': 'Server error'}, status=500)

        return self.get_response(request)

    def _should_check_jwt(self, path):
        # Add paths that don't need JWT verification
        public_paths = [
            '/api/auth/',
            '/api/public/',
            '/admin/',
            '/docs/',
        ]
        return not any(path.startswith(prefix) for prefix in public_paths)

def jwt_required(roles=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user_role'):
                return JsonResponse({'error': 'Authentication required'}, status=401)

            if roles and request.user_role not in roles:
                return JsonResponse({'error': 'Insufficient permissions'}, status=403)

            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

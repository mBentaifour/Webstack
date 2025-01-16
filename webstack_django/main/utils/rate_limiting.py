from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
from django.conf import settings
import time

class CustomRateThrottle(SimpleRateThrottle):
    """
    Custom rate throttle that can be applied to views or viewsets
    """
    cache_format = 'throttle_%(scope)s_%(ident)s'
    
    def __init__(self, rate=None, scope=None):
        self.rate = rate or settings.API_RATE_LIMIT
        self.scope = scope or 'user'
        super().__init__()
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
            
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class BurstRateThrottle(CustomRateThrottle):
    """
    Allows bursts of requests but then enforces a cooling period
    """
    scope = 'burst'
    
    def allow_request(self, request, view):
        if getattr(view, 'throttle_scope', None):
            self.scope = view.throttle_scope

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = cache.get(self.key, [])
        now = time.time()

        # Drop any requests from the history which are now outside the window
        while self.history and self.history[-1] <= now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return False

        self.history.insert(0, now)
        cache.set(self.key, self.history, self.duration)
        return True

# Example usage in views:
"""
from rest_framework.decorators import throttle_classes

@throttle_classes([CustomRateThrottle])
class MyAPIView(APIView):
    throttle_scope = 'my_api'  # Define custom scope
    
    def get(self, request):
        # Your view logic here
        pass
"""

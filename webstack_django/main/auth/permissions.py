from rest_framework import permissions
from functools import wraps

class RoleBasedPermission(permissions.BasePermission):
    """
    Permission class that checks if the user has the required roles
    """
    def __init__(self, required_roles):
        self.required_roles = required_roles

    def has_permission(self, request, view):
        if not request.auth:
            return False
            
        user_roles = request.auth.get('roles', [])
        return any(role in user_roles for role in self.required_roles)

def require_roles(*roles):
    """
    Decorator for views that checks if the user has any of the specified roles
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.auth:
                return permissions.IsAuthenticated().has_permission(request, None)
                
            user_roles = request.auth.get('roles', [])
            if not any(role in user_roles for role in roles):
                return permissions.IsAuthenticated().has_permission(request, None)
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Predefined permission classes for common roles
class IsAdmin(RoleBasedPermission):
    def __init__(self):
        super().__init__(['admin'])

class IsStaff(RoleBasedPermission):
    def __init__(self):
        super().__init__(['admin', 'staff'])

class IsCustomer(RoleBasedPermission):
    def __init__(self):
        super().__init__(['customer'])

# Object-level permissions
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.auth and 'admin' in request.auth.get('roles', []):
            return True
            
        return obj.user_id == request.auth.get('user_id')

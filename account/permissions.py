from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    """Permission basée sur les rôles."""
    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = "Vous devez être connecté pour accéder à cette ressource."
            return False
        if request.user.role not in self.allowed_roles:
            self.message = f"Accès refusé : rôle requis ({', '.join(self.allowed_roles)})."
            return False
        return True

class IsOwner(BasePermission):
    """Permission pour les propriétaires."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

class IsAdmin(BasePermission):
    """Permission pour les administrateurs."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'owner']

class IsManagerSales(BasePermission):
    """Permission pour les managers des ventes."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['manager_sales', 'admin', 'owner']

class IsManagerStock(BasePermission):
    """Permission pour les managers du stock."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['manager_stock', 'admin', 'owner']

class IsCashier(BasePermission):
    """Permission pour les caissiers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['cashier', 'admin', 'owner']

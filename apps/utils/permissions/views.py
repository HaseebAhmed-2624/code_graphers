from rest_framework.permissions import BasePermission, AllowAny



class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = "Access denied for unauthenticated users"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsUnAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = "Access denied for authenticated users"

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)



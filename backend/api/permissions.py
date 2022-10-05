from rest_framework import permissions


class AdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Права доступа: Администратор или Автор или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.user.is_superuser
                or obj.author == request.user
            )
        return False

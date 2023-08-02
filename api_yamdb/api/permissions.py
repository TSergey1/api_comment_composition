from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Класс права доступа только админу или чтение
    для Title, Categories, Ganrez.
    """
    def has_permission(self, request, view): 
        return (request.method in permissions.SAFE_METHODS 
                or (request.user.is_authenticated and ( 
                    request.user.is_admin or request.user.is_superuser)))


class IsAuthorOrAdminOrModeratOrReadOnly(permissions.BasePermission):
    """
    Класс права доступа админу, модератору, автору или для чтение
    для Comments, Review.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
                )


class IsAdmin(permissions.BasePermission):
    """Класс права доступа админу, суперюзера."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)

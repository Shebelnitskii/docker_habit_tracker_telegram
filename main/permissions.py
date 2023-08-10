from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пользователь может работать только со своими привычками."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsPublicOrReadOnly(permissions.BasePermission):
    """Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять."""

    def has_object_permission(self, request, view, obj):
        if obj.public == True:
            return True
        elif obj.public == False and obj.owner != request.user:
            return False
        else:
            return False
from rest_framework import permissions


class IsOwnerOrAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return post.writer == request.user or request.user.is_superuser

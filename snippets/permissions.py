from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow read access to public snippets, and full access only to owners."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for public snippets.
        if request.method in permissions.SAFE_METHODS:
            if obj.is_private:
                return obj.owner == request.user
            return True

        # Write permissions are only allowed to the owner.
        return obj.owner == request.user

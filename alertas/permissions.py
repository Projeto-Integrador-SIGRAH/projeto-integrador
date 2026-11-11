from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.groups.filter(name="CIDADAO").exists()
            and obj.user == request.user
        )


# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

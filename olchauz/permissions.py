from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PATCH', 'PUT', 'DELETE']:
            return request.user.is_authenticated

        if request.method in 'POST':
            return request.user.is_authenticated
        return False
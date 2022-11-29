from rest_framework import permissions


class APIPermission(permissions.BasePermission):
    message = 'No access to this network object!'

    def has_permission(self, request, view):
        if request.user.is_active == True:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.employees.id == request.auth.user_id:
            return True
        return False

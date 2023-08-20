from rest_framework import permissions

class AdminOrPostOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user.is_authenticated and request.user.is_staff
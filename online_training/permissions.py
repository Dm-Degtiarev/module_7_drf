from rest_framework import permissions


class ModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модератор').exists():
            if request.method in ('DELETE', 'POST'):
                return False
            return True

class OwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False
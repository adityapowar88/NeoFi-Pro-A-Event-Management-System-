from rest_framework import permissions
from .models import EventPermission

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class HasEventPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            event_perm = EventPermission.objects.get(event=obj, user=request.user)
            if request.method in permissions.SAFE_METHODS:
                return event_perm.role in ['viewer', 'editor', 'owner']
            elif request.method in ['PUT', 'PATCH']:
                return event_perm.role in ['editor', 'owner']
            elif request.method == 'DELETE':
                return event_perm.role == 'owner'
        except EventPermission.DoesNotExist:
            return False
        return False

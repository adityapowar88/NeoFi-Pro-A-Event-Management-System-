from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from events.models import Event
from .serializers import ShareEventSerializer
from django.shortcuts import get_object_or_404
from .serializers import EventPermissionSerializer
from events.models import EventPermission
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

User = get_user_model()


class ShareEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        event = get_object_or_404(Event, id=id)

        if not event.permissions.filter(user=request.user, role='owner').exists():
            return Response({"detail": "Only owners can share this event."}, status=403)

        serializer = ShareEventSerializer(data=request.data, context={'event': event})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User added/updated successfully."}, status=200)
        
        return Response(serializer.errors, status=400)

class EventPermissionsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        event = get_object_or_404(Event, id=id)

        if not event.permissions.filter(user=request.user).exists():
            return Response({"detail": "Access denied."}, status=403)

        permissions_qs = EventPermission.objects.filter(event=event).select_related('user')
        serializer = EventPermissionSerializer(permissions_qs, many=True)
        return Response(serializer.data)
    
    
class UpdateEventPermissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id, userId):
        event = get_object_or_404(Event, id=id)

        owner_permission = EventPermission.objects.filter(event=event, user=request.user, role='owner').first()
        if not owner_permission:
            return Response({"detail": "Only the owner can update roles."}, status=403)

        target_user = get_object_or_404(User, id=userId)

        try:
            permission = EventPermission.objects.get(event=event, user=target_user)
        except EventPermission.DoesNotExist:
            return Response({"detail": "User does not have permission for this event."}, status=404)

        new_role = request.data.get("role")
        if new_role not in dict(EventPermission.ROLE_CHOICES):
            return Response({"detail": "Invalid role."}, status=400)

        permission.role = new_role
        permission.save()

        return Response({"detail": f"Role updated to '{new_role}' for user {target_user.username}."})

class EventPermissionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, userId):
        event = get_object_or_404(Event, id=id)
        if not EventPermission.objects.filter(event=event, user=request.user, role='owner').exists():
            return Response({'detail': 'Only the event owner can remove permissions.'}, status=status.HTTP_403_FORBIDDEN)

        permission = get_object_or_404(EventPermission, event=event, user__id=userId)
        permission.delete()
        return Response({'detail': 'Permission removed successfully.'}, status=status.HTTP_204_NO_CONTENT)

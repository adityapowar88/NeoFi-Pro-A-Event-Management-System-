from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from events.models import Event
from .models import EventVersion
from .serializers import EventVersionSerializer
from events.permissions import HasEventPermission
from rest_framework import permissions

class EventVersionDetailView(APIView):
    def get(self, request, id, versionId):
        event = get_object_or_404(Event, pk=id)
        version = get_object_or_404(EventVersion, event=event, version_number=versionId)
        serializer = EventVersionSerializer(version)
        permission_classes = [permissions.IsAuthenticated, HasEventPermission]
        return Response(serializer.data)

class EventRollbackView(APIView):
    def post(self, request, id, versionId):
        event = get_object_or_404(Event, pk=id)
        version = get_object_or_404(EventVersion, event=event, version_number=versionId)

        event.title = version.title
        event.description = version.description
        event.start_time = version.start_time
        event.end_time = version.end_time
        event.location = version.location
        event.is_recurring = version.is_recurring
        event.recurrence_pattern = version.recurrence_pattern
        event.save()

        return Response({"detail": f"Rolled back to version {versionId}"})


class EventChangeLogView(APIView):
    def get(self, request, id):
        event = get_object_or_404(Event, pk=id)
        
        versions = EventVersion.objects.filter(event=event).order_by('version_number')
        
        serializer = EventVersionSerializer(versions, many=True)
        return Response(serializer.data)
    

class EventVersionDiffView(APIView):
    def get(self, request, id, versionId1, versionId2):
        event = get_object_or_404(Event, pk=id)

        # Fetch both versions
        version1 = get_object_or_404(EventVersion, event=event, version_number=versionId1)
        version2 = get_object_or_404(EventVersion, event=event, version_number=versionId2)

        # Convert to dicts
        v1_data = EventVersionSerializer(version1).data
        v2_data = EventVersionSerializer(version2).data

        # Compute differences
        diff = {}
        for field in v1_data:
            if v1_data[field] != v2_data[field]:
                diff[field] = {
                    "version1": v1_data[field],
                    "version2": v2_data[field]
                }

        return Response(diff)

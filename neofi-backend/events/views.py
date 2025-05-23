from rest_framework import generics, permissions,filters
from .models import Event, EventPermission
from .serializers import EventSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework import viewsets
from .filters import EventFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination
from .permissions import HasEventPermission


# Create a new event 
class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.save(owner=self.request.user, created_by=self.request.user)
        EventPermission.objects.create(event=event, user=self.request.user, role='owner')


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ['is_recurring', 'recurrence_pattern']
    ordering_fields = ['start_time', 'end_time', 'title']
    search_fields = ['title', 'description', 'location']
    pagination_class = CustomPagination


    def get_queryset(self):
        return Event.objects.filter(
            permissions__user=self.request.user
        ).distinct()


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated ,HasEventPermission]

    def get_object(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'], permissions__user=self.request.user)
        return event
    

class ConflictException(APIException):
    status_code = 409
    default_detail = "Conflict: The resource was modified by another process."
    default_code = "conflict"

class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        client_timestamp = request.data.get("last_updated")

        if client_timestamp:
            client_dt = parse_datetime(client_timestamp)
            if client_dt and instance.updated_at > client_dt:
                raise ConflictException()

        return super().update(request, *args, **kwargs)

class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])

        try:
            permission = EventPermission.objects.get(event=event, user=self.request.user)
        except EventPermission.DoesNotExist:
            raise PermissionDenied("You do not have permission to delete this event.")

        if permission.role != 'owner':
            raise PermissionDenied("Only the owner can delete this event.")

        return event


class BatchEventCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        events_data = request.data.get('events', [])

        if not isinstance(events_data, list):
            return Response({"error": "Expected a list of events"}, status=status.HTTP_400_BAD_REQUEST)

        created_events = []
        errors = []

        for event_data in events_data:
            serializer = EventSerializer(data=event_data)
            if serializer.is_valid():
                event = serializer.save(owner=request.user)
                EventPermission.objects.create(event=event, user=request.user, role='owner')
                created_events.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"created": created_events, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)

        return Response({"created": created_events}, status=status.HTTP_201_CREATED)

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Event
from datetime import datetime, timedelta

class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_event_creation(self):
        event = Event.objects.create(
            title="Test Event",
            owner=self.user,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=2),
            location="Test Location"
        )
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.owner, self.user)

from django.test import TestCase
from .models import Event

class EventModelTest(TestCase):
    def setUp(self):
        Event.objects.create(title="Test Event")

    def test_event_creation(self):
        event = Event.objects.get(title="Test Event")
        self.assertEqual(event.title, "Test Event")

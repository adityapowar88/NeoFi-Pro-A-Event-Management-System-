from django.db import models
from events.models import Event

class EventVersion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="versions")
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    version_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.event.title} - v{self.version_number}"

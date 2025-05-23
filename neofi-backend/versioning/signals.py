# versioning/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Event
from .models import EventVersion

@receiver(post_save, sender=Event)
def create_event_version(sender, instance, created, **kwargs):
    latest_version = EventVersion.objects.filter(event=instance).order_by('-version_number').first()
    version_number = 1 if not latest_version else latest_version.version_number + 1

    EventVersion.objects.create(
        event=instance,
        version_number=version_number,
        title=instance.title,
        description=instance.description,
        start_time=instance.start_time,
        end_time=instance.end_time,
        location=instance.location,
        is_recurring=instance.is_recurring,
        recurrence_pattern=instance.recurrence_pattern
    )

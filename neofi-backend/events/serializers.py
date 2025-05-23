from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_time', 'end_time', 'location',
            'is_recurring', 'recurrence_pattern', 'owner', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_by', 'created_at', 'updated_at']

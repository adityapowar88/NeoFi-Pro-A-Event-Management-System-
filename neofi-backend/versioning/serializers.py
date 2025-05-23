from rest_framework import serializers
from .models import EventVersion

class EventVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVersion
        fields = '__all__'

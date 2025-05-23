from rest_framework import serializers
from events.models import EventPermission
from django.contrib.auth import get_user_model
User = get_user_model()

class ShareEventSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=EventPermission.ROLE_CHOICES)

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found.")
        return value

    def create(self, validated_data):
        event = self.context['event']
        user = User.objects.get(id=validated_data['user_id'])
        permission, created = EventPermission.objects.update_or_create(
            event=event,
            user=user,
            defaults={'role': validated_data['role']}
        )
        return permission


class EventPermissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = EventPermission
        fields = ['user', 'role']

        
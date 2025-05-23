from django_filters import rest_framework as django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="start_time", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="end_time", lookup_expr='lte')
    is_recurring = django_filters.BooleanFilter(field_name="is_recurring")

    class Meta:
        model = Event
        fields = ['start_date', 'end_date', 'is_recurring']

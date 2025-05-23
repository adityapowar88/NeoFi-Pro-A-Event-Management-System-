from django.urls import path
from .views import ShareEventView,EventPermissionsListView,UpdateEventPermissionView,EventPermissionDeleteView

urlpatterns = [
    path('<int:id>/share', ShareEventView.as_view(), name='event-share'),
    path('<int:id>/permissions', EventPermissionsListView.as_view(), name='event-permissions'),
    path('<int:id>/permissions/<int:userId>', UpdateEventPermissionView.as_view(), name='event-permission-update'),
    path('<int:id>/permissions/<int:userId>/delete', EventPermissionDeleteView.as_view(), name='remove-permission'),
]

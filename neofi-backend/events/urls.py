from django.urls import path
from .views import EventCreateView, EventListView, EventDetailView, EventUpdateView, EventDeleteView, BatchEventCreateView

urlpatterns = [
    path('', EventCreateView.as_view(), name='event-create'),
    path('list', EventListView.as_view(), name='event-list'), 
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'), 
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),  
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),  
    path('batch/', BatchEventCreateView.as_view(), name='event-batch-create'),  

]

from django.urls import path
from .views import EventVersionDetailView, EventRollbackView, EventChangeLogView, EventVersionDiffView

urlpatterns = [
    path('<int:id>/changelog', EventChangeLogView.as_view(), name='event-changelog'),
    path('<int:id>/diff/<int:versionId1>/<int:versionId2>', EventVersionDiffView.as_view(), name='event-diff'),
    path('<int:id>/history/<int:versionId>', EventVersionDetailView.as_view()),
    path('<int:id>/rollback/<int:versionId>', EventRollbackView.as_view()),
]

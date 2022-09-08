from django.urls import path
from .views import UploadView, VideoListView, SearchSubtitlesView

urlpatterns = [
    path('', UploadView.as_view(), name="home"),
    path('videos/', VideoListView.as_view(), name="videos"),
    path('search/<str:subtitle_id>/', SearchSubtitlesView.as_view(), name="search"),
]
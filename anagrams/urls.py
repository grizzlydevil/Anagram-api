from django.urls import path

from .views import ListAnagramsAPIView

urlpatterns = [
    path(
        '<slug:word>.json',
        ListAnagramsAPIView.as_view()
    ),
]

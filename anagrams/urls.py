from django.urls import path

from . views import ListAnagramsAPIView

urlpatterns = [
    path(
        r'(?P<word>\w+).json',
        ListAnagramsAPIView.as_view()
    ),
]

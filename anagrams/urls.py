from django.urls import path

from .views import ListAnagramsAPIView, CheckIfWordsAreAnagramsView

urlpatterns = [
    path(
        '<slug:word>.json',
        ListAnagramsAPIView.as_view()
    ),
    path('check_anagrams/words.json', CheckIfWordsAreAnagramsView.as_view())
]

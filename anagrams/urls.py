from django.urls import path

from .views import ListDeleteAnagramsAPIView, CheckIfWordsAreAnagramsView

urlpatterns = [
    path(
        '<slug:word>.json',
        ListDeleteAnagramsAPIView.as_view()
    ),
    path('check-anagrams/words.json', CheckIfWordsAreAnagramsView.as_view())
]

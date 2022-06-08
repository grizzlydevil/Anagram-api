from django.urls import path, include

from rest_framework import routers

from .views import (
    CreateDeleteCorpusViewSet, ShowCorpusStatsView, GetAnagramsView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('', CreateDeleteCorpusViewSet, basename='corpus')

urlpatterns = [
    path('', include(router.urls)),
    path('stats.json', ShowCorpusStatsView.as_view()),
    path('get-anagrams.json', GetAnagramsView.as_view())
]

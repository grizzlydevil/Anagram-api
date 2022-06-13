from django.urls import path, include

from rest_framework import routers

from .views import (
    CreateDeleteCorpusViewSet, ShowCorpusStatsView, GetAnagramsView
)

app_name = "data"

router = routers.DefaultRouter(trailing_slash=False)
router.register('', CreateDeleteCorpusViewSet, basename='corpus')

urlpatterns = [
    path('', include(router.urls)),
    path('stats.json', ShowCorpusStatsView.as_view(), name='stats'),
    path('get-anagrams.json', GetAnagramsView.as_view(), name='get-anagrams')
]

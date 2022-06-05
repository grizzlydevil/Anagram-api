from rest_framework import routers

from .views import CreateDeleteCorpusViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', CreateDeleteCorpusViewSet, basename='corpus')

urlpatterns = router.urls

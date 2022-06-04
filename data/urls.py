from rest_framework import routers

from .views import CreateDeleteCorpusViewSet

router = routers.SimpleRouter()
router.register('', CreateDeleteCorpusViewSet, basename='corpus')

urlpatterns = router.urls

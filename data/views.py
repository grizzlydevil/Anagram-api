from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from .serializers import CorpusSerializer


class CreateDeleteCorpusViewSet(
    GenericViewSet, CreateModelMixin, DestroyModelMixin
):
    """A viewset to store and delete words to the corpus"""

    serializer_class = CorpusSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.words, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status.HTTP_201_CREATED)

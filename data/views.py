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
        words = request.data

        if not words['words'] and len(words['words']) > 0:
            content = {'error': 'words list not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # words = [{'word': word} for word in words]
        serializer = self.get_serializer(data=words)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

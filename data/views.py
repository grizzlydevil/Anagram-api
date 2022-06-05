from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CorpusSerializer


class CreateDeleteCorpusViewSet(
    GenericViewSet, CreateModelMixin
):
    """A viewset to store and delete words to the corpus"""

    serializer_class = CorpusSerializer

    def create(self, request):
        words = request.data.get('words')

        if not words or len(words) == 0:
            content = {'error': 'words list not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='')
    def delete_corpus(self, request):
        pass

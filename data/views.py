from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .serializers import CorpusSerializer
from .models import Corpus


class CreateDeleteCorpusViewSet(GenericViewSet):
    """A viewset to store and delete words to the corpus"""

    serializer_class = CorpusSerializer

    @action(detail=False, methods=['post', 'delete'], url_path='words')
    def create_delete_corpus(self, request):
        if request.method == 'DELETE':
            Corpus.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        words = request.data.get('words')

        if not words or len(words) == 0:
            content = {'error': 'words list not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['delete'],
        url_path=r'words/(?P<word>\w+).json',
        url_name='word'
    )
    def delete_word(self, _, word):
        word_obj = Corpus.objects.filter(word=word)
        if len(word_obj) == 1:
            self.perform_destroy(word_obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, obj):
        obj.delete()

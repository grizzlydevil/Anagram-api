from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from data.models import Corpus
from .serializers import AnagramsSerializer


class ListAnagramsAPIView(ListAPIView):
    """List specified word anagrams limits results with limit query param"""
    serializer_class = AnagramsSerializer
    queryset = Corpus.objects.all()

    def list(self, request, *args, **kwargs):
        word = kwargs.get('word')
        limit = request.GET.get('limit')
        if limit and (not limit.isdigit() or int(limit) < 1):
            data = {
                'error':
                    'limit query param should integer and be greater than 0'
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)

        limit = int(limit) if limit else None

        hash = Corpus.get_hash(word)
        letter_chain = Corpus.get_alphagram(word)

        queryset = self.get_queryset().filter(hash=hash)
        if queryset:
            all_words = [item.word for item in queryset
                         if item.word != word and
                         Corpus.get_alphagram(item.word) == letter_chain]

            if limit:
                all_words = all_words[:limit]

        serializer = AnagramsSerializer(all_words)
        return Response(serializer.data)

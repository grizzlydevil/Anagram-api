from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from data.models import Corpus
from .serializers import AnagramsSerializer


class ListAnagramsAPIView(ListAPIView):
    """List specified word anagrams limits results with limit query param"""
    serializer_class = AnagramsSerializer
    queryset = Corpus.objects.all()

    def list(self, request, *args, **kwargs):
        word = kwargs.get('word')
        limit = request.GET.get('limit')
        limit = int(limit) if limit and limit.isnumeric() else limit

        hash = Corpus.get_hash(word)
        letter_chain = Corpus.get_alphagram(word)

        queryset = self.get_queryset()
        queryset = (queryset.filter(hash=hash)
                    .exclude(word=word)
                    .filter(alphagram__chain=letter_chain))

        if limit:
            queryset = queryset[:limit]

        serializer = AnagramsSerializer(queryset)
        return Response(serializer.data)

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from data.models import Corpus
from .serializers import WordSerializer


class ListAnagramsAPIView(ListAPIView):
    """List specified word anagrams limits results with limit query param"""
    serializer_class = WordSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = WordSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        word = self.request
        limit = self.request.GET.get('Limit')

        hash = Corpus.get_hash(word)
        letter_chain = Corpus.get_alphagram(word)

        queryset = (
            Corpus.objects
            .filter(hash=hash)
            .exclude(word=word)
            .filter(alphagram_chain=letter_chain)
        )

        if limit:
            queryset[:limit]

        return queryset

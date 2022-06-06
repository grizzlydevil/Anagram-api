import timeit

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
        if limit and not limit.is_numeric() and int(limit) < 1:
            data = {'error': 'limit query param should be greater than 0'}
            return Response(data, status.HTTP_400_BAD_REQUEST)

        limit = int(limit) if limit else None

        hash = Corpus.get_hash(word)
        letter_chain = Corpus.get_alphagram(word)

        starttime = timeit.default_timer()
        queryset = self.get_queryset()
        for i in range(20):
            queryset = (queryset.filter(hash=hash))
            # queryset = (queryset.filter(hash=hash)
            #             .exclude(word=word)
            #             .filter(alphagram__chain=letter_chain))
            # queryset = (queryset.filter(alphagram__chain=letter_chain)
            #             .exclude(word=word)
            #             )
            print(
                ", ".join(
                    [item.word for item in queryset]
                ) if len(queryset) > 0 else 'NONE'
            )
        print(timeit.default_timer() - starttime)

        if limit:
            queryset = queryset[:limit]

        serializer = AnagramsSerializer(queryset)
        return Response(serializer.data)

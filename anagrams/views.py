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

        hash = Corpus.get_hash(word)

        queryset = self.get_queryset().filter(hash=hash)
        all_words = {}
        if queryset.exists():
            all_words = [item.word for item in queryset
                         if item.word != word]

            limit = int(limit) if limit else None
            if limit:
                all_words = all_words[:limit]

            include_proper_nouns = request.GET.get('include_proper_nouns')
            if include_proper_nouns and include_proper_nouns == 'False':
                all_words = [word for word in all_words if word.islower()]

        serializer = AnagramsSerializer(all_words)
        return Response(serializer.data)

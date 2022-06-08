import re

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from data.models import Corpus
from .serializers import AnagramsSerializer
from data.serializers import CorpusSerializer


class ListAnagramsAPIView(ListAPIView):
    """List specified word anagrams limits results with limit query param"""
    serializer_class = AnagramsSerializer
    queryset = Corpus.objects.all()

    def list(self, request, *args, **kwargs):
        word = kwargs.get('word')
        limit = request.GET.get('limit')
        if limit and (not limit.isdigit() or int(limit) < 1):
            content = {
                'error':
                    'limit query param should integer and be greater than 0'
            }
            return Response(content, status.HTTP_400_BAD_REQUEST)

        # check if word contains illegal characters
        if not re.match('^[a-zA-Z-]+$', word):
            content = {
                'error':
                    'specified word contains illegal characters'
            }
            return Response(content, status.HTTP_400_BAD_REQUEST)

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


class CheckIfWordsAreAnagramsView(APIView):
    """A view that returns if posted list of words are anagrams"""

    def post(self, request):
        words = request.data.get('words')

        if not words or len(words) < 2:
            content = {'error': 'words list not found or too few words'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = CorpusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content = {
            'words': words,
            'all_words_are_anagrams': self.words_are_anagrams(words)
        }
        return Response(content, status=status.HTTP_200_OK)

    def words_are_anagrams(self, words):
        hashes = [Corpus.get_hash(word) for word in words]

        return all(hash == hashes[0] for hash in hashes[1:])

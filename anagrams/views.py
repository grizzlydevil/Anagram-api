import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from data.models import Corpus
from data.serializers import CorpusSerializer


class ListDeleteAnagramsAPIView(APIView):
    """List specified word anagrams limits results with limit query param"""

    def get(self, request, *args, **kwargs):
        word = kwargs.get('word')
        limit = request.GET.get('limit')
        if limit and (not limit.isdigit() or int(limit) < 1):
            content = {
                'error':
                    'limit query param should integer and be greater than 0'
            }
            return Response(content, status.HTTP_400_BAD_REQUEST)

        self.check_for_illegal_characters(word)

        hash = Corpus.get_hash(word)

        queryset = Corpus.objects.filter(hash=hash)
        anagrams = []
        if queryset.exists():
            anagrams = [item.word for item in queryset
                        if item.word != word]

            include_proper_nouns = request.GET.get('include_proper_nouns')
            if include_proper_nouns and include_proper_nouns == 'False':
                anagrams = [word for word in anagrams if word.islower()]

            limit = int(limit) if limit else None
            if limit:
                anagrams = anagrams[:limit]

        content = {
            'anagrams': anagrams
        }

        return Response(content, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Delete a word and all of it's anagrams"""
        word = kwargs.get('word')

        self.check_for_illegal_characters(word)
        hash = Corpus.get_hash(word)

        words_to_delete = Corpus.objects.filter(hash=hash)
        content = {
            'deleted': list(words_to_delete.values_list('word', flat=True))
        }
        words_to_delete.delete()

        return Response(content, status=status.HTTP_204_NO_CONTENT)

    def check_for_illegal_characters(self, word):
        if not re.match('^[a-zA-Z-]+$', word):
            content = {
                'error':
                    'specified word contains illegal characters'
            }
            return Response(content, status.HTTP_400_BAD_REQUEST)


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

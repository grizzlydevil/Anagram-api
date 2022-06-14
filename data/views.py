from django.db.models import Avg, Max, Min, Count
from django.db.models.functions import Length

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    CorpusSerializer
)
from .models import Corpus


class CreateDeleteCorpusViewSet(GenericViewSet):
    """A viewset to manipulate data in the Corpus"""

    serializer_class = CorpusSerializer

    @action(
        detail=False,
        methods=['post', 'delete'],
        url_path='words',
        url_name='words'
    )
    def create_delete_corpus(self, request):
        if request.method == 'DELETE':
            Corpus.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        words = request.data.get('words')

        if not words or not isinstance(words, list) or len(words) == 0:
            content = {'error': 'words list not found'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if words[0] == 'ingest dict':
            """This is a hack to store the whole dictionary.txt to DB"""
            with open('data/dictionary.txt', 'r') as file:
                words = file.readlines()

            words = [word.strip() for word in words]
            serializer = self.get_serializer(data={'words': words})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['delete'],
        url_path=r'words/(?P<word>\w+)',
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


class ShowCorpusStatsView(APIView):
    """
    Endpoint that returns a count of words in the corpus and
    min/max/median/average word length
    """

    def get(self, request):
        stats = self.get_object()

        return Response(stats, status=status.HTTP_200_OK)

    def get_object(self):
        queryset = Corpus.objects.all()

        if queryset.exists():
            queryset = queryset.annotate(length=Length('word')
                                         ).order_by('length')
            num_of_words = queryset.count()
            stats = queryset.aggregate(
                min_length=Min('length'),
                average_length=Avg('length'),
                max_length=Max('length'),
            )

            median_index = int(num_of_words / 2)
            if num_of_words % 2 == 0:
                stats['median_length'] = (
                    (queryset[median_index - 1].length +
                     queryset[median_index].length) / 2
                )
            else:
                stats['median_length'] = (
                    queryset[median_index].length
                )

            stats['word_count'] = num_of_words

        return stats


class GetAnagramsView(APIView):
    """A view that shows groups of words with most anagrams"""

    def get(self, request):
        size = request.GET.get('size')
        data = self.get_object(size)

        return Response(data, status=status.HTTP_200_OK)

    def get_object(self, size):
        queryset = Corpus.objects.all()
        obj = {}

        if queryset.exists():
            hashes_sorted_by_popularity = (
                queryset
                .values('hash')
                .annotate(count=Count('id'))
                .order_by('-count')
            )

            # if size is not specified most popular will be collected
            group_size = (
                size if size else hashes_sorted_by_popularity[0]['count']
            )

            most_popular_groups = (
                hashes_sorted_by_popularity.filter(
                    count__gte=group_size)
            )

            most_popular_hashes = [
                hash['hash'] for hash in most_popular_groups]

            queryset = queryset.filter(hash__in=most_popular_hashes)
            obj = {
                'words_with_most_anagrams':
                [list(queryset.filter(hash=single_hash)
                 .values_list('word', flat=True))
                 for single_hash in most_popular_hashes]
            }

        return obj

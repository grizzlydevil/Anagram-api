from rest_framework import serializers

from .models import Corpus


class CorpusSerializer(serializers.Serializer):

    words = serializers.ListField()

    def validate_words(self, words):
        """validate words"""

        # create unique words list
        unique_words = list(set(words))

        # Is it a single word? Does it contain illeagal characters?
        for word in unique_words:
            match = Corpus.check_for_illegal_characters(word)
            if not match:
                raise serializers.ValidationError(
                    'one or more words have illegal characters'
                )

        # Is word in English language?

        return unique_words

    def create(self, validated_data):
        """
        Creating a new word database entry the hash and an alphagram will be
        added
        """

        words = validated_data['words']
        corpus = []
        for word in words:

            # do not enter the same words into corpus
            if Corpus.objects.filter(word=word).exists():
                continue

            hash = Corpus.get_hash(word)

            corpus.append(
                Corpus(word=word, hash=hash)
            )

        return Corpus.objects.bulk_create(corpus)


class CorpusStatsSerializer(serializers.Serializer):

    word_count = serializers.IntegerField()
    min_length = serializers.IntegerField()
    max_length = serializers.IntegerField()
    average_length = serializers.DecimalField(max_digits=5, decimal_places=2)
    median_length = serializers.DecimalField(max_digits=4, decimal_places=1)

import re

from rest_framework import serializers

from .models import Corpus, Alphagram


class CorpusSerializer(serializers.Serializer):

    words = serializers.ListField()

    def validate_words(self, words):
        """validate words"""

        # create unique words list
        unique_words = list(set(words))

        # Is it a single word? Does it contain illeagal characters?
        for word in unique_words:
            match = re.match('^[a-zA-Z]+$', word)
            if not match:
                unique_words.remove(word)
                # raise serializers.ValidationError(
                #     'one or more words have illegal characters'
                # )

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
            letter_chain = Corpus.get_alphagram(word)

            alphagram, _ = Alphagram.objects.get_or_create(
                letter_chain=letter_chain
            )

            corpus.append(
                Corpus(word=word, hash=hash, alphagram=alphagram)
            )

        return Corpus.objects.bulk_create(corpus)


class CorpusStatsSerializer(serializers.Serializer):

    word_count = serializers.IntegerField()
    min_length = serializers.IntegerField()
    max_length = serializers.FloatField()
    average_length = serializers.IntegerField()
    median_length = serializers.FloatField()


class WordsWithMostAnagramsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return instance

import re

from rest_framework import serializers

from .models import Corpus
from .models import Alphagram


class CorpusSerializer(serializers.Serializer):

    words = serializers.ListField()

    def validate_words(self, words):
        """validate words"""
        # Is it a single word? Does it contain illeagal characters?
        for word in words:
            match = re.search('^[a-zA-Z]$', word)
            if not match:
                raise serializers.ValidationError(
                    'one or more words have illeagal characters'
                )

        # Is word in English language?
        return words

    def create(self, validated_data):
        """
        Creating a new word database entry the hash and an alphagram will be
        added
        """

        words = validated_data['words']
        corpus = []
        for word in words:
            lowercase_word = word.lower()
            hash = sum(
                (1 << (ord(letter) - 97) * 2 for letter in lowercase_word)
            )
            alphagram = ''.join(sorted(lowercase_word))

            alphagram_obj, _ = Alphagram.objects.get_or_create(
                chain=alphagram
            )

            corpus.append(
                Corpus(word=word, hash=hash, alphagram=alphagram_obj)
            )

        return Corpus.objects.bulk_create(corpus)

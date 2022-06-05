import re

from rest_framework import serializers

from .models import Corpus
from .models import Alphagram


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

            lowercase_word = word.lower()
            hash = sum(
                (1 << (ord(letter) - 97) * 2 for letter in lowercase_word)
            )
            chain = ''.join(sorted(lowercase_word))

            alphagram, _ = Alphagram.objects.get_or_create(
                chain=chain
            )

            corpus.append(
                Corpus(word=word, hash=hash, alphagram=alphagram)
            )

        return Corpus.objects.bulk_create(corpus)

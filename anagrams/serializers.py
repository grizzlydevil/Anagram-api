from rest_framework import serializers

from data.models import Corpus


class AnagramsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        words = [word_obj.word for word_obj in instance]
        return {
            'anagrams': words
        }

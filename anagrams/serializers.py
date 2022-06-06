from rest_framework import serializers

from data.models import Corpus


class AnagramsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'anagrams': instance
        }

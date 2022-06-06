from rest_framework import serializers


class AnagramsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'anagrams': instance
        }

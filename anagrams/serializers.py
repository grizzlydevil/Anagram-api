from rest_framework import serializers

from data.models import Corpus


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = ('word',)

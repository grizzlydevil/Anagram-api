from django.db import models


class Corpus(models.Model):
    """A model for word. To match against anagrams stores hash and alphagram"""

    word = models.CharField(max_length=50)
    hash = models.PositiveBigIntegerField(db_index=True)

    @staticmethod
    def get_hash(word):
        return sum(
                (1 << (ord(letter) - 97) * 2 for letter in word.lower())
        )

    @staticmethod
    def get_alphagram(word):
        return ''.join(sorted(word.lower()))

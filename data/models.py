from django.db import models


class Alphagram(models.Model):
    """
    An alphagram is a string with all the letters in the word sorted in
    alphabetic order
    """

    chain = models.CharField(max_length=50, unique=True)


class Corpus(models.Model):
    """A model for word. To match against anagrams stores hash and alphagram"""

    word = models.CharField(max_length=50)
    hash = models.PositiveBigIntegerField()

    alphagram = models.ForeignKey(Alphagram, on_delete=models.CASCADE)

    @classmethod
    def get_hash(word):
        return sum(
            (1 << (ord(letter) - 97) * 2 for letter in word.lower())
        )

    @classmethod
    def get_anagram(word):
        return ''.join(sorted(word.lower()))

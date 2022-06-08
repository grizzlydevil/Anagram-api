from django.db import models


class Corpus(models.Model):
    """A model for word. To match against anagrams stores hash and alphagram"""

    word = models.CharField(max_length=50)
    hash = models.PositiveBigIntegerField(db_index=True)

    @staticmethod
    def get_hash(word):
        """
        Create a hash to store in the database which would be unique to every
        anagram
        """
        lowercase_word = word.lower().replace('-', '')

        # every letter of a word is hashed as a bitwise number
        # every letter has 2 bits corresponding to the times this letter
        # appeared in the word.
        word_hash = sum((1 << (ord(letter) - 97) * 2
                         for letter in lowercase_word))

        # However in the rare cases when there is for example 4 letters 'a' in
        # the word the word hash would be the same as letter 'b'
        # For this purpose I also hash the length of a word
        length_of_word = len(lowercase_word)

        # shiftig 6 bits to the left and adding word length
        # 6 bits lets hashing word up to 63 letters long. Which is plenty
        # enough for English language
        hash_with_word_length = (word_hash << 6) | length_of_word

        return hash_with_word_length

    @staticmethod
    def get_alphagram(word):
        return ''.join(sorted(word.lower()))

import math

from statistics import median

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Corpus


CREATE_DELETE_CORPUS_URL = reverse('data:corpus-words')
STATS_URL = reverse('data:stats')
GET_ANAGRAMS_URL = reverse('data:get-anagrams')


class CreateCorpusTests(TestCase):
    """Test creating corpus"""

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'words': [
                'parleys',
                'parsley',
                'players',
                'replays',
                'sparely'
            ]
        }

    def add_words(self, words=None):
        return self.client.post(
            CREATE_DELETE_CORPUS_URL,
            data=words if words else self.data
        )

    def test_create_corpus(self):
        """Test creating corpus and seeing it's data in the stats"""

        response = self.add_words()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        all_words = Corpus.objects.all()
        self.assertTrue(all(word.hash > 0 for word in all_words))

        words = list(all_words.values_list('word', flat=True))
        self.assertListEqual(sorted(self.data['words']), sorted(words))

    def test_adding_same_words(self):
        """Test adding same words to corpus"""
        data = {
            'words': [
                'replays',
                'sparely',
                'add',
                'add',
                'new',
                'words'
            ]
        }
        response = self.add_words(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check that old words are still unique
        old_word_occurencies = Corpus.objects.filter(word='replays').count()
        self.assertEqual(old_word_occurencies, 1)

        # check if new words were added and only one instance
        new_word_occurencies = Corpus.objects.filter(word='new').count()
        self.assertEqual(new_word_occurencies, 1)

    def test_delete_word(self):
        """Test deleting a word from corpus"""

        word = 'new'
        delete_word_url = reverse('data:corpus-word', args=[word])
        response = self.client.delete(delete_word_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Corpus.objects.filter(word=word).exists())

    def test_words_with_illegal_chars(self):
        """Test adding words with illegal characters"""
        data = {'words': ['hi5']}
        response = self.add_words(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'words': ['two words']}
        response = self.add_words(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_words_with_legal_chars(self):
        """Test adding words with legal characters"""

        data = {'words': [
            "word's", 'word-master'
        ]}
        response = self.add_words(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_corpus(self):
        """Test deleting the whole corpus"""

        response = self.client.delete(CREATE_DELETE_CORPUS_URL)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Corpus.objects.all().exists())


class StatsTests(TestCase):
    """Test stats are returning factual data"""

    def setUp(self):
        self.client = APIClient()
        self.data = {
            'words': [
                'a',
                'bb',
                'ccc',
                'dddd',
                'eeeee',
            ]
        }
        self.client.post(CREATE_DELETE_CORPUS_URL, data=self.data)

    def get_data_dict(self, data=None):
        data = data if data else self.data
        data_dict = {}

        word_count = len(self.data['words'])
        data_dict['word_count'] = word_count

        word_length = [len(word) for word in self.data['words']]

        data_dict['min_length'] = min(word_length)
        data_dict['max_length'] = max(word_length)
        data_dict['average_length'] = sum(word_length) / word_count
        data_dict['median_length'] = median(sorted(word_length))

        return data_dict

    def test_stats(self):
        """Test stats data"""

        response = self.client.get(STATS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictEqual(self.get_data_dict(), response.data)

        # add new word to test for even and odd num of words
        new_word = 'newbie'

        # add new word to corpus
        self.client.post(
            CREATE_DELETE_CORPUS_URL,
            data={'words': [new_word]}
        )

        response = self.client.get(STATS_URL)

        words = self.data
        words['words'].append(new_word)

        self.assertDictEqual(self.get_data_dict(words), response.data)

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from data.tests import BaseTestCaseSetUp
from data.models import Corpus

WORDS_ANAGRAMS_URL = reverse('anagrams:words-anagrams')
WORDS = ['lapser', 'parles', 'pearls']


class GetDeleteAnagramsTests(BaseTestCaseSetUp):
    """Test getting and deleting anagrams"""

    def test_get_anagrams(self):
        # these anagrams are checked: 'lapser', 'parles', 'pearls'
        url = reverse('anagrams:anagrams', args=['lapser'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response should contain:
        should_contain = ['parles', 'pearls']

        self.assertEqual(sorted(should_contain),
                         sorted(response.data['anagrams']))

    def test_delete_word_and_anagrams(self):
        """Check if word is deleted and all of its anagrams"""

        # plaser is non existing word that would have anagrams
        # 'lapser', 'parles', 'pearls'
        # nothing should be deleted as the word doesn't exist
        url = reverse('anagrams:anagrams', args=['plaser'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # check if these words still exist were not deleted
        num = Corpus.objects.filter(word__in=WORDS).count()

        self.assertEqual(num, len(WORDS))

        # check deleting an existing word
        url = reverse('anagrams:anagrams', args=['lapser'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check if words were deleted
        num = Corpus.objects.filter(word__in=WORDS).count()
        self.assertEqual(num, 0)


class WordsAreAnagramsTests(APITestCase):
    """Check CheckIfWordsAreAnagramsView works as intended"""

    def setUp(self):
        self.data = {
            'words': WORDS
        }

    def post_words(self, words):
        return self.client.post(WORDS_ANAGRAMS_URL, data=words, format='json')

    def test_words_are_anagrams(self):
        """Check with words that are anagrams"""

        response = self.post_words(self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data['all_words_are_anagrams'])

    def test_words_are_not_anagrams(self):
        """Check with words that are not anagrams"""

        self.data['words'].append("grizzly")
        response = self.post_words(self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(response.data['all_words_are_anagrams'])

    def test_no_word_list_posted(self):
        """Check if wrong post params will not work somehow"""

        data = {'some': WORDS}
        response = self.post_words(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'words': 'WORDS'}
        response = self.post_words(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'words': ['WORDS']}
        response = self.post_words(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

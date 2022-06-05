from rest_framework.generics import ListAPIView

from data.models import Corpus


class ListAnagrams(ListAPIView):
    """List specified word anagrams limits results with limit query param"""

    def list(self, request):
        pass

    def get_queryset(self):
        word = self.request
        limit = self.request

        hash = Corpus.get_hash(word)
        letter_chain = Corpus.get_alphagram(word)

        queryset = (
            Corpus.objects
            .filter(hash=hash)
            .exclude(word=word)
            .filter(alphagram_chain=letter_chain)
        )

        if limit:
            queryset[:limit]

        return queryset

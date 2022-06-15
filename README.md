# Set Up
 - Create an empty folder for project.
 - bash in project folder
 > git clone https://github.com/grizzlydevil/Anagram-api.git


# Anagram-api

Endpoints:
- `POST /words.json`: Takes a JSON array of English-language words and adds them to the corpus (data store).
json format: { "words": ["read", "dear", "dare"] }

- `DELETE /words.json`: Deletes all contents of the data store. (no turning back..)

- `DELETE /words/{word}.json`: Deletes a single word from the data store.

- `GET /anagrams/{word}.json?limit=5&include_proper_nouns=False`:
  Returns a JSON array of English-language words that are anagrams of the word passed in the URL.
  This endpoint supports `limit=1` an optional query param that indicates the maximum number of results to return.
  It also supports `include_proper_nouns=False` optional query param that filters proper nouns. By default it is set to True

- `DELETE /anagrams/{word}.json`: Deletes a word and all of it's anagrams from the corpus. The word must exist in the corpus.

- `GET /stats.json`: Endpoint that returns a count of words in the corpus and min/max/median/average word length.

- `GET /get-anagrams.json`: Endpoint that returns word groups with most words as anagrams from the corpus.
 - This endpoint supports `size=5` query param which then returns not only most popular groups but all groups of words and their anagrams of specified size or more words in them.

- `POST /anagrams/check-anagrams/words.json`: Takes a JSON array of English-language words and returns a json response whether they are all anagrams.
- response json format:
```
{
    "words": [
        "read",
        "dear",
        "dare"
    ],
    "all_words_are_anagrams": true
}
```
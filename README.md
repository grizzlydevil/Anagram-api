# Set Up

- Create an empty folder for project.
- Open bash in project folder
> git clone https://github.com/grizzlydevil/Anagram-api.git

- Create a new virtual environment in the project folder
- Activate env
> pip install -r requirements.txt

- The project uses PostgreSQL. It needs to be set up in the anagram_api/settings.py DATABASES
> python manage.py migrate

- Check if the project is working
> python manage.py test

- Run server
> python manage.py runserver

# Anagram-api

Endpoints:
- `POST /words.json`: Takes a JSON array of English-language words and adds them to the corpus (data store).
json format: { "words": ["read", "dear", "dare"] }
There is a secret json to post which makes the database to ingest the whole dictionaty.txt you provided. (**WARNING** This might take 10-15 mins)
> { "words": ["ingest dict"] }

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

# Notes

```
This API is limited to words only. Anagrams can theoretically contain multiple words this is not implemented right now.
Words inside corpus currently can contain special characters apostrophe and hyphen ['-]. But these characters are not included in the anagram hash calculation. For example word o'clock and imaginary word cloock would be anagrams.
For every word put into corpus a hash is generated which is unique for every anagram word. This hash is set as index in the database. This approach makes database searches very fast. In my testing I noticed that queries return around 3x quicker than making a query with VARCHAR strings.
```

# The hash

```
The hash is created as a bitmap. English language consists of 25 letters and I provided 2 bits for every letter.
2 bits are needed to be able to encode multiples of the same letter. Giving it 2 bits enables encoding up to 3 of the same letter. If for example a word has 4 a letters they will be encoded the same as a letter b.
For that reason At the end or 50 bits I added 6 more bits to encode the length of the word.
The max word length limitation at the moment is 63 characters (6 bits). Which I thought was plenty enough for english language.
Storing this as a decimal positive integer creates a unique hash which as far as I can see only another anagram could have.
It enables pretty quick database search.
```

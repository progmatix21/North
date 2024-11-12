# North

The art or study of correct spelling according to usage is orthography.
How often are we obsessed with seeing the correct spellings of words
when we use them, and how good it would be if you had an automated
means to do that.  Here comes 'North' an app which rhymes with 'orth'
of 'orthography'.

North is a trie-based ASCII sequence suggester.  It uses the Damerau-Levenshtein
algorithm to select the closest match.

## Usage

You can use North as an arbitrary (ASCII) sequence checker/suggester.

- **As a spell checker.**  First, initialize the class North 
with a list of valid spellings.  It will then suggest the closest matches
to an arbitrary misspelled word.
- **Arbitrary sequence checker.** It can also be used as a rough check for 
long, closely matching DNA sequences.

Here is an example of importing and using North:

```python
from north import North

correct_word_list = ["Hayagreeva","Rama","Red","Violet","Blue","Green","Hanuman","Sugreeva",
                     "Bangalore","Bengaluru","India","Indianapolis","New Delhi"]

misspelled_word_list = ["Hanugreeva","hanman","Indiia","Bengalure","New Deli","Viola","Bloo"]

my_spelling_suggester = North(correct_word_list)

for misspelled_word in misspelled_word_list:
    print(misspelled_word, my_spelling_suggester(misspelled_word,topn=2))
```

```
Hanugreeva ('Sugreeva', 'Hanuman')
hanman ('Hanuman',)
Indiia ('India', 'Indianapolis')
Bengalure ('Bengaluru', 'Bangalore')
New Deli ('New Delhi',)
Viola ('Violet', 'Rama')
Bloo ('Blue',)
```

## Installation

Install the `pytrie` package for the trie functionality.
Install the `fastDamerauLevenshtein` for the similarity algorithm.

There is a `requirements.txt` file which you can optionally use with pip3.


Then clone this repository and start using North.



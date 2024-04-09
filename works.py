from nltk.corpus import wordnet as wn

def expand_query(query):
    synsets = wn.synsets(query)
    synonyms = set()
    hypernyms = set()
    hyponyms = set()
    meronyms = set()
    holonyms = set()
    antonyms = set()

    for synset in synsets:
        synonyms.update(synset.lemma_names())
        hypernyms.update(synset.hypernyms())
        hyponyms.update(synset.hyponyms())
        meronyms.update(synset.part_meronyms())
        holonyms.update(synset.part_holonyms())
        antonyms.update(synset.lemmas()[0].antonyms())

    return {
        'Synonyms': synonyms,
        'Hypernyms': hypernyms,
        'Hyponyms': hyponyms,
        'Meronyms': meronyms,
        'Holonyms': holonyms,
        'Antonyms': antonyms
    }

query = input("Enter a word to expand: ")
expanded_query = expand_query(query)
print(expanded_query)

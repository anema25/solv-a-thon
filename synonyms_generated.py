import pandas as pd
from nltk.corpus import wordnet

# Function to generate synonyms for a word
def generate_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return ', '.join(synonyms)

# Load CSV file
df = pd.read_csv('/workspaces/solv-a-thon/modified_file_new.csv')

# Generate synonyms for each word in the "words" column and store in a new column "Synonyms"
df['Synonym_'] = df['Words'].apply(lambda x: ', '.join(generate_synonyms(word) for word in str(x).split(',')))

# Save updated DataFrame to CSV
df.to_csv('output_file.csv', index=False)

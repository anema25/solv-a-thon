import pandas as pd
from nltk.corpus import wordnet as wn

# Function to expand query and gather synonyms
def expand_query(query):
    synsets = wn.synsets(query)
    synonyms = set()

    for synset in synsets:
        synonyms.update(synset.lemma_names())

    return ', '.join(synonyms)  # Join synonyms into a comma-separated string

# Load CSV file
df = pd.read_csv('your_csv_file.csv')

# Process each word separately and store synonyms in a new column
df['Synonyms'] = df['words'].apply(lambda x: ', '.join(expand_query(word) for word in str(x).split(',')))

# Print all synonyms of the input query
query = input("Enter a word to expand: ")
query_synonyms = expand_query(query)
print("Synonyms of '{}': {}".format(query, query_synonyms))

# Compare query synonyms with the "Synonyms" column and print corresponding values of "name"
matched_rows = df[df['Synonyms'].apply(lambda x: query_synonyms in x.split(', '))]
matched_names = matched_rows['name'].tolist()
print("Matching names from 'name' column:", matched_names)

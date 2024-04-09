import pandas as pd
from nltk.corpus import wordnet as wn
from difflib import SequenceMatcher

# Function to calculate similarity between two strings
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to expand query and gather synonyms
def expand_query(query):
    synsets = wn.synsets(query)
    synonyms = set()

    for synset in synsets:
        synonyms.update(synset.lemma_names())

    return ', '.join(synonyms)  # Join synonyms into a comma-separated string

# Load CSV file
df = pd.read_csv('/workspaces/solv-a-thon/output_file.csv')

# Process each word separately and store synonyms in a new column
df['Synonyms'] = df['Words'].apply(lambda x: ', '.join(expand_query(word) for word in str(x).split(',')))

# Print all synonyms of the input query
query = input("Enter a word to expand: ")
query_synonyms = expand_query(query)
print("Synonyms of '{}': {}".format(query, query_synonyms))

# Calculate similarity between query synonyms and "Synonyms" column
df['Similarity'] = df['Synonyms'].apply(lambda x: similarity(x, query_synonyms))

# Find highest similarity value's corresponding name column value
highest_similarity_row = df[df['Similarity'] == df['Similarity'].max()]
highest_similarity_name = highest_similarity_row['Name'].iloc[0]
highest_similarity_value = highest_similarity_row['Similarity'].iloc[0]

# Print highest similarity value's corresponding name column value and similarity value
print("Highest Similarity Name:", highest_similarity_name)
print("Highest Similarity Value:", highest_similarity_value)

# Print all similarity values
print("Similarity Values:")
print(df[['Name', 'Similarity']])

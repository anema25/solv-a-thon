import nltk
import pandas as pd
from nltk.corpus import wordnet

# Download WordNet data
nltk.download('wordnet')

# Load the CSV file into a DataFrame
df = pd.read_csv('/workspaces/solv-a-thon/check.csv')

# Function to find synonyms of a word
def find_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# User input for the keyword
user_keyword = input("Enter a keyword: ")

# Find synonyms of the user input keyword
synonyms_list = find_synonyms(user_keyword)
print(f"Synonyms of '{user_keyword}': {', '.join(synonyms_list)}")

# Check if any synonym matches with words in the 'Synonym_' column of the DataFrame
matches = []
for synonym in synonyms_list:
    matches.extend(df[df['Synonym_'].str.contains(synonym, na=False)].to_dict(orient='records'))

# Print the matching names and the matched words
if matches:
    print("\nMatching names and matched words:")
    for match in matches:
        print(f"Name: {match['Name']}, Matched Word(s): {match['Synonym_']}")
else:
    print("\nNo matches found.")

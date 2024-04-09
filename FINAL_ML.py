import nltk
import pandas as pd
from nltk.corpus import wordnet

# Download WordNet data
nltk.download('wordnet')

# Load the CSV file into a DataFrame
df = pd.read_csv('/workspaces/solv-a-thon/merged_with_synonyms.csv')

# Function to find synonyms of a word
def find_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Function to merge the content of 'Words' and 'Synonym_' columns into a single column
def merge_synonyms(row):
    return f"{row['Words']}, {row['Synonym_']}"

# Apply the merge_synonyms function to create a new column 'merge_synonyms'
df['merge_synonyms'] = df.apply(merge_synonyms, axis=1)

# User input for the keyword
user_keyword = input("Enter a keyword: ").lower()  # Convert user input to lowercase

# Find synonyms of the user input keyword
synonyms_list = find_synonyms(user_keyword)
print(f"Synonyms of '{user_keyword}': {', '.join(synonyms_list)}")

# Check if any synonym matches with words in the 'merge_synonyms' column of the DataFrame
matched_professors = set()
for synonym in synonyms_list:
    matches = df[df['merge_synonyms'].str.lower().str.contains(synonym.lower(), na=False)]
    matched_professors.update(matches['Name'].tolist())

# Print the matching professor names
if matched_professors:
    print("\nMatching professor names:")
    for professor in matched_professors:
        print(professor)
else:
    print("\nNo matches found.")

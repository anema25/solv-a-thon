import csv
import spacy

# Load spaCy's English language model
nlp = spacy.load('en_core_web_sm')

def calculate_similarity(keyword, domain):
    # Process the keyword and domain text using spaCy
    keyword_doc = nlp(keyword)
    domain_doc = nlp(domain)

    # Calculate similarity between the keyword and domain
    similarity = keyword_doc.similarity(domain_doc)
    return similarity

# User input for the keyword
user_keyword = input("Enter a keyword: ")

max_score = float('-inf')
max_domain_name = None
all_scores = {}

# Open the CSV file and calculate similarity scores
with open('processors_domains.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        domain_name = row['Domain']
        similarity_score = calculate_similarity(user_keyword, domain_name)
        all_scores[domain_name] = similarity_score

        if similarity_score > max_score:
            max_score = similarity_score
            max_domain_name = domain_name

# Print the domain with the highest score and all scores
print(f"The domain with the highest score for '{user_keyword}' is '{max_domain_name}' with a score of {max_score}")
print("All scores:")
for domain, score in all_scores.items():
    print(f"{domain}: {score}")

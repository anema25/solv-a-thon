import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website containing professors' profiles
url = 'https://example.com/professors'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all elements containing professor profiles (adjust based on website structure)
professor_elements = soup.find_all('div', class_='professor-profile')

# Initialize lists to store data
names = []
research_areas = []
publications = []
contact_info = []

# Extract data from each professor profile
for professor in professor_elements:
    name = professor.find('h2').text.strip()
    names.append(name)
    
    research_area = professor.find('div', class_='research-area').text.strip()
    research_areas.append(research_area)
    
    publications_list = [pub.text.strip() for pub in professor.find_all('li', class_='publication')]
    publications.append(publications_list)
    
    contact = professor.find('div', class_='contact-info').text.strip()
    contact_info.append(contact)

# Create a DataFrame from the extracted data
df = pd.DataFrame({
    'Name': names,
    'Research Area': research_areas,
    'Publications': publications,
    'Contact Info': contact_info
})

# Save DataFrame to a CSV file
df.to_csv('professors_data.csv', index=False)

print('Professors data saved to professors_data.csv')

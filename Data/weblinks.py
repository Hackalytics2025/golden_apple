import requests
from bs4 import BeautifulSoup
import json

# URL of the index page with all Apple iPhone models
url = "https://howmuch.one/phones"

# Get the HTML content of the page
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to retrieve page, status code {response.status_code}")

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize an empty dictionary to store model names and links
iphone_links = {}

# Find all anchor tags on the page
for a in soup.find_all('a'):
    # Get the text and check if it starts with "Apple iPhone"
    model_name = a.get_text(strip=True)
    if model_name.startswith("Apple iPhone"):
        href = a.get('href')
        if href:
            # Convert relative URLs to absolute URLs if needed
            href = requests.compat.urljoin(url, href)
            iphone_links[model_name] = href

# Save the data to a JSON file
with open("iphone_links.json", "w") as json_file:
    json.dump(iphone_links, json_file, indent=2)

print("iPhone model links have been saved to iphone_links.json")

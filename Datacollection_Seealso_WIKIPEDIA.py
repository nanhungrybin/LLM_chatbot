import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Function to extract content from a given URL
def extract_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all("p")
        text = " ".join(paragraph.get_text() for paragraph in paragraphs)
        return text
    else:
        return "Content could not be retrieved."

# Base Wikipedia URL
base_url = "https://en.wikipedia.org"

# Specific page to start from
page = "/wiki/Injection_moulding"

# Initialize list to store data
data_list = []

# Make a request to fetch the HTML content of the page
response = requests.get(base_url + page)

# Verify successful request
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the 'See also' section
    see_also_section = soup.find("span", {"id": "See_also"}).find_next("ul")
    
    if see_also_section:
        links = see_also_section.find_all("a")
        
        for link in links:
            link_title = link.get("title")
            link_url = base_url + link.get("href")
            
            # Extract content from the link URL
            link_content = extract_content(link_url)
            
            print(link_content)
            
            # Get current date and time
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Define data structure for the current link
            data = {
                'contents': {
                    'title': link_title,
                    'text': link_content
                },
                'link': link_url,
                'source': 'Wikipedia',
                'date': now,
                'language': 'English'
            }
            
            # Append data to the list
            data_list.append(data)

# Save data to JSON file
with open('C:\\Users\\InterX_2team\\Desktop\\HB\\0401_Crawling\\Seealso_wikipedia.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print(f"Data saved to 'see_also_links_content.json'. Total links processed: {len(data_list)}")

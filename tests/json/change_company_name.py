

import json

import requests
from bs4 import BeautifulSoup




with open("tests/json/urls_output_list_full.json", "r") as file:
    data = json.load(file)



HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"'
}

def get_web_title(url):
    try:
        corrected_url = url.replace('www.www.', 'www.')  # Correcting the www.www issue
        response = requests.get("http://" + corrected_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup.title:  # Checking if title is not None before fetching string
            return soup.title.string
        else:
            return "No title found"
    except Exception as e:
        print(f"Error fetching title for {corrected_url}. Error: {e}")
        return None

for item in data:
    url = item.get("URL")
    if url:
        title = get_web_title(url)
        if title:
            item["Company's Name"] = title
            print(title,'got')

# Print the updated JSON
print(json.dumps(data, indent=4))
with open('tests/json/company_names.json', 'w') as file:
    json.dump(data, file, indent=4)
    'WH Ireland – Helping you see the bigger picture'
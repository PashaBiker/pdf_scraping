import json
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# with open("tests/json/test.json", "r") as file:
with open("tests/json/urls_output_list_full.json", "r") as file:
    data = json.load(file)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"'
}

def get_web_title(item):
    try:
        url = item.get("URL")
        if not url:
            return None, None

        corrected_url = url.replace('www.www.', 'www.')
        response = requests.get("http://" + corrected_url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else "No title found"
        return title, item
    except Exception as e:
        print(f"Error fetching title for {corrected_url}. Error: {e}")
        return None, None

# Using ThreadPoolExecutor to speed up the process
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url = {executor.submit(get_web_title, item): item for item in data}
    for future in concurrent.futures.as_completed(future_to_url):
        title, item = future.result()
        if title and item:
            item["Title"] = title.strip()
            print(title, 'got')

# Save the updated JSON
with open('tests/json/company_names3.json', 'w') as file:
    json.dump(data, file, indent=4)



# No title
# No title found
# Home - 
# Home | 
# 403 Forbidden 
# Gmail
# 404 Page no found
# Site Not Configured | 404 Not Found
# Untitled Document
# Homepage - 
# Web Server's Default Page 
# Bot Verification 
# Apache2 Ubuntu Default Page: It works 
# 404 - File or directory not found. 
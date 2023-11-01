import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_web_title(session, url):
    try:
        corrected_url = url.replace('www.www.', 'www.')
        
        # Use this line if you want to bypass SSL verification (not recommended for production)
        # async with session.get("http://" + corrected_url, headers=HEADERS, ssl=False) as response:
        
        async with session.get("http://" + corrected_url, headers=HEADERS) as response:
            content = await response.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            if soup.title:
                return soup.title.string
            else:
                return "No title found"
    except aiohttp.client_exceptions.ClientConnectorError as e:
        # Handle domain resolution and connection refusal errors
        print(f"Connection error for {corrected_url}. Error: {e}")
    except aiohttp.client_exceptions.ClientSSLError as e:
        # Handle SSL errors
        print(f"SSL error for {corrected_url}. Error: {e}")
    except Exception as e:
        # Handle other errors
        print(f"Error fetching title for {corrected_url}. Error: {e}")
    return None
# async def get_web_title(session, url):
#     try:
#         corrected_url = url.replace('www.www.', 'www.')
#         async with session.get("http://" + corrected_url, headers=HEADERS) as response:
#             content = await response.read()
#             soup = BeautifulSoup(content, 'html.parser')
            
#             if soup.title:
#                 return soup.title.string
#             else:
#                 return "No title found"
#     except Exception as e:
#         print(f"Error fetching title for {corrected_url}. Error: {e}")
#         return None

async def fetch_titles(data):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in data:
            url = item.get("URL")
            if url:
                task = asyncio.create_task(get_web_title(session, url))
                tasks.append(task)
        
        titles = await asyncio.gather(*tasks)

        for item, title in zip(data, titles):
            if title:
                item["Company's Name"] = title
                print(title, 'got')

        return data

with open("tests/json/urls_output_list_full.json", "r") as file:
    data = json.load(file)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"'
}

updated_data = asyncio.run(fetch_titles(data))

# Print the updated JSON
print(json.dumps(updated_data, indent=4))

with open('tests/json/company_names.json', 'w') as file:
    json.dump(updated_data, file, indent=4)

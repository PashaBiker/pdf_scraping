import json
import asyncio
import httpx
from bs4 import BeautifulSoup

with open("tests/json/urls_output_list_full.json", "r") as file:
    data = json.load(file)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"'
}

async def get_web_title(item):
    url = item.get("URL")
    if url:
        corrected_url = url.replace('www.www.', 'www.')
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://" + corrected_url, headers=HEADERS)
                
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.title:
                title = soup.title.string
                item["Company's Name"] = title
                print(title, 'got')
            else:
                print(f"No title found for {corrected_url}")
        except Exception as e:
            print(f"Error fetching title for {corrected_url}. Error: {e}")

async def main():
    # Create tasks for each URL to fetch titles concurrently
    tasks = [get_web_title(item) for item in data]
    await asyncio.gather(*tasks)

# Run the async functions
asyncio.run(main())

# Save the updated data
with open('tests/json/company_names.json', 'w') as file:
    json.dump(data, file, indent=4)

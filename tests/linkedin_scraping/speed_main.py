import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

file_path = 'uk_output.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    json_data = json.load(file)

def get_linkedin_link(query):
    # query = query  + ' UK'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'NID=511=dgOjXbuVHfX3Rbkdg7MkWhCRCAUmMBKlHhw2CAPyOTqJGCYq8vOemkmSpFd2BmlH8hXmc5-3HHdKcQc-5gfPu3BrTFDx3jbdxoM-B_dp5HQNudbF_bM4QX38YDqs9r9rH_AHbjmTpYnwBtDA-PuEMIcdh3fgi9FrJeh4EigSIOc',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.199", "Google Chrome";v="120.0.6099.199"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.5.6"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # 'x-client-data': 'CI62yQEIpLbJAQipncoBCPH1ygEIlKHLAQiHoM0BCNy9zQEIusjNAQjI6c0BCOTszQEIzu7NAQiD8M0BCIbwzQEIqPLNARj2yc0BGKfqzQE=',
    }
    params = {
        'q': query,
        'pq': query,
        # 'sourceid': 'chrome',
        # 'ie': 'UTF-8',
    }

    response = requests.get('https://www.bing.com/search', params=params, headers=headers)
    # response = requests.get('https://www.google.com/search', params=params, headers=headers)
    # print('responce given', query)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        href = link['href']
        # print(href)
        exclusions = ['/images/', '/pub/', '/posts/', '/redir/', '/company/', '/school/', '/pulse/']
        # Check if the href does not contain any of the exclusions
        if 'linkedin' in href and '/in/' in href and not any(exclusion in href for exclusion in exclusions):            # print(href)
            return href
    return None

def update_json_data(item):
    linkedin_link = get_linkedin_link(item["allname"])
    if linkedin_link:
        print(f"LinkedIn link for {item['allname']}: {linkedin_link}")
        item["ActualLinkedIn"] = linkedin_link
    return item

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=14) as executor:
        results = list(executor.map(update_json_data, json_data))

    updated_json_data_with_actual_linkedin = json.dumps(results, indent=4)
    file_name = 'UK_updated_data_with_linkedin.json'
    with open(file_name, 'w') as file:
        file.write(updated_json_data_with_actual_linkedin)

    print('Finished updating JSON data with LinkedIn links.')

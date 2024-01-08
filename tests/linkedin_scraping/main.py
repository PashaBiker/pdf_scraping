import requests
from bs4 import BeautifulSoup
import json

file_path = 'tests/linkedin_scraping/output.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    json_data = json.load(file)


# The search query
def get_linkedin_links(query):
    headers = {
        'authority': 'www.google.com',
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
        'x-client-data': 'CI62yQEIpLbJAQipncoBCPH1ygEIlKHLAQiHoM0BCNy9zQEIusjNAQjI6c0BCOTszQEIzu7NAQiD8M0BCIbwzQEIqPLNARj2yc0BGKfqzQE=',
    }

    params = {
        'q': query,
        'oq': query,
        'sourceid': 'chrome',
        'ie': 'UTF-8',
    }

    response = requests.get('https://www.google.com/search', params=params,headers=headers)

    # Parsing the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    linked_in_links = []
    # Finding the first link
    first_link = soup.findAll('a', href=True)
    for link in first_link:
        if 'linkedin' in link['href'] and 'translate.google' not in link['href'] and '/pub/' not in link['href'] and '/posts/' not in link['href']:
            linked_in_links.append(link['href'])
    print(linked_in_links)
    return linked_in_links[0]

if __name__ == "__main__":
    for item in json_data:
        linkedin_link = get_linkedin_links(item["allname"])
        print(linkedin_link)
        item["ActualLinkedIn"] = linkedin_link
    updated_json_data_with_actual_linkedin = json.dumps(json_data, indent=4)
    file_name = 'updated_data.json'
    with open(file_name, 'w') as file:
        file.write(updated_json_data_with_actual_linkedin)
    print('finished')


from concurrent.futures import ThreadPoolExecutor

import json
import logging
import re
from bs4 import BeautifulSoup

import requests


file_path = 'tests/linkedin_scraping/first_part.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    json_data = json.load(file)

    # The search query
def get_title_name(query):

    pattern = r"/in/([^/?]+)"

    # Extracting the required part using regex
    extracted_part = re.search(pattern, str(query))
    result = extracted_part.group(1) if extracted_part else "Not found"


    query = result + ' linkedin UK'
    print(query)
    headers = {
        'authority': 'www.bing.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'MUID=37E25B36D56368D7312248C9D41969A2; MUIDB=37E25B36D56368D7312248C9D41969A2; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=A1C73BA6730F4529927D727B0482AF6D&dmnchg=1; _UR=QS=0&TQS=0; _EDGE_S=SID=300875E08EEF69BE0519661F8F3F68E5&mkt=ru-ru; _SS=SID=300875E08EEF69BE0519661F8F3F68E5; SRCHUSR=DOB=20240107&T=1704666647000&TPC=1704629211000; ipv6=hit=1704670247956&t=4; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wMS0wN1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjo2LCJUb2JuIjowfQ==; SRCHHPGUSR=SRCHLANG=en&IG=969515F6A63F448FB74D8A7F731C9359&BRW=HTP&BRH=M&CW=1001&CH=961&SCW=1164&SCH=1764&DPR=1.0&UTC=120&DM=1&WTS=63840263447&PV=6.5.6&HV=1704666799&PRVCW=1001&PRVCH=961',
        'referer': f'https://www.bing.com/search?q={query}',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"120.0.6099.199"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.199", "Google Chrome";v="120.0.6099.199"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.5.6"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'q': query,
        'pq': query,
        'qs': 'n',
        'form': 'QBRE',
        'sp': '-1',
        'lq': '0',
        'sc': '10-32',
        'sk': '',
        'cvid': '8F6D2C2D360D4ED8ABAA6AB579B85C23',
        'ghsh': '0',
        'ghacc': '0',
        'ghpl': '',
    }


    response = requests.get('https://www.bing.com/search', params=params,headers=headers)

    # Parsing the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    works_for = None
    title = None

    # Try to find "Works For"
    try:
        works_for_span = soup.find('span', title=lambda x: x and x.startswith('Works For:'))
        if works_for_span:
            works_for = works_for_span['title'].replace('Works For:', '').strip()
    except:
        pass

    if not works_for:
        try:
            works_for_div = soup.find('strong', text='Works For:').parent
            if works_for_div:
                works_for = works_for_div.get_text(strip=True).replace('Works For:', '').strip()
        except:
            pass


    # print(soup)
    # Try to find "Title"
    try:
        title_div = soup.find('strong', text='Title:')
        if title_div:
            title = title_div.get_text(strip=True).replace('Title:', '').strip()
    except:
        pass
    # Try to find "Job Title" if "Title" is not found
    if not title:
        try:
            job_title_span = soup.find('strong', text=lambda text: text and 'Job Title' in text)
            if job_title_span:
                job_title_container = job_title_span.parent
                if job_title_container:
                    job_title_text = job_title_container.get_text(strip=True)
                    if ':' in job_title_text:
                        title = job_title_text.split(':', 1)[1].strip()
        except:
            pass

    if not title:
        try:
            # Extract "Job Title"
            job_title_div = soup.find('strong', text='Occupation:')
            # print(job_title_div)
            if job_title_div:
                title = job_title_div.find_next_sibling(text=True).strip()
        except:
            pass
    # Print results
    if works_for:
        print(f"Works For: {works_for}")
    else:
        print("Works For information not found")

    if title:
        print(f"Title: {title}")
    else:
        print("Title information not found")
    
    return title, works_for
        
def update_json_data(item):
    title, works_for = get_title_name(item["ActualLinkedIn"])
    if title or works_for:
        print(f"LinkedIn title and works for {item['allname']}: {title}, {works_for}")
        item["LinkedIn Title"] = title
        item["working for"] = works_for
    return item


# if __name__ == "__main__":
#     with ThreadPoolExecutor(max_workers=22) as executor:
#         results = list(executor.map(update_json_data, json_data))

#     updated_json_data_with_actual_linkedin = json.dumps(results, indent=4)
#     file_name = 'title_worksfor.json'
#     with open(file_name, 'w') as file:
#         file.write(updated_json_data_with_actual_linkedin)

#     print('Finished updating JSON data with LinkedIn links.')
if __name__ == "__main__":
    results = []
    try:
        with ThreadPoolExecutor(max_workers=22) as executor:
            results = list(executor.map(update_json_data, json_data))
    except Exception as e:
        logging.error("An error occurred during processing: %s", e)
        print("An error occurred. Partial results will be saved.")
    finally:
        # This block executes whether an exception occurs or not
        updated_json_data_with_actual_linkedin = json.dumps(results, indent=4)
        file_name = 'title_worksfor.json'
        with open(file_name, 'w') as file:
            file.write(updated_json_data_with_actual_linkedin)
        print('JSON data saved to file:', file_name)
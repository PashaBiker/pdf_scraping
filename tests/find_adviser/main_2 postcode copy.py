import json
from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import openpyxl
import threading

headers = {
    'authority': 'www.thepfs.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ASP.NET_SessionId=vlwrepr0nccrbnrghafatrkw; visid_incap_2922113=fv/PvTD8R56ihX1RGHGd4BfnP2UAAAAAQUIPAAAAAABUm63nCKDgOi62tl8kbGJr; incap_ses_259_2922113=yqj1bekkNSO3pQ8aWyiYAxjnP2UAAAAAgVf+NxCmVsuKTo9SqeosrQ==; _gcl_au=1.1.932214066.1698686745; _gid=GA1.2.1380339841.1698686745; _ga=GA1.2.1427429530.1698686745; _ga_3MKZKX1842=GS1.1.1698686745.1.1.1698686870.6.0.0; _gali=googlePlaceholder',
    'origin': 'https://www.thepfs.org',
    'referer': 'https://www.thepfs.org/yourmoney/find-an-adviser/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}
session = requests.Session()
session.headers.update(headers)

# Set up a global cache for geolocation results
geo_cache = {}
def get_lat_lon(postcode, country="UK"):
    if postcode in geo_cache:
        return geo_cache[postcode]

    geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    
    full_address = f"{postcode}, {country}"

    try:
        location = geolocator.geocode(full_address, timeout=10)
        if location:
            geo_cache[postcode] = (location.latitude, location.longitude)
            return location.latitude, location.longitude
        else:
            geo_cache[postcode] = (None, None)
            return None, None
    except GeocoderTimedOut:
        print("Error: geocode failed due to time out")
        return None, None

def extract_column_data(file_name, column_letter, sheet_name=None):
    workbook = openpyxl.load_workbook(file_name)
    if sheet_name:
        sheet = workbook[sheet_name]
    else:
        sheet = workbook.active
    data = [cell.value for cell in sheet[column_letter] if cell.value is not None]
    workbook.close()
    return data

def scrape_data_for_postcode(postcode):
    lat, lon = get_lat_lon(postcode)
    if not lat or not lon:
        return None

    data = {
        'advisorLocation': 'Test',
        'lat': lat,
        'lng': lon,
        'withContactDetails': 'on',
        'specialism': 'Investing',
    }

    response = session.post('https://www.thepfs.org/yourmoney/find-an-adviser/', data=data)
    html_data = response.content
    soup = BeautifulSoup(html_data, 'html.parser')
    
    all_data = []
    for li in soup.find_all('li'):
        # print(li)
        # breakpoint()
        # Extract manager's name
        managers_name = None
        managers_name_li = li.find('h3', class_='adviser-name')
        if managers_name_li:
            managers_name = managers_name_li.text.strip()
        email_tag_div = li.find('div', class_='yui3-u adv-item adv-email')

        email = None
        if email_tag_div:  # Check if the div was found
            # print(email_tag_div)
            email_tag = email_tag_div.find('a', href=True, attrs={'href': lambda x: x.startswith('mailto:')})
            if email_tag:
                # print(email_tag)
                email = email_tag['href'].replace('mailto:', '')
                # print(email)

        # Extract company's name from email
        companys_name = None
        if email:
            domain_with_tld = email.split('@')[1]
            companys_name = domain_with_tld.split('.')[0]
        
        # Extract phone number
        phone_elem = li.find('div', class_='yui3-u adv-item adv-telephone')
        phone_number = phone_elem.text.strip() if phone_elem else None

        # Extract address and postcode
        address_elem = li.find('a', class_='showGoogle')
        address, postcode = None, None
        if address_elem:
            address_contents = [content.strip() for content in address_elem.stripped_strings]
            postcode = address_contents[-2]  # Assuming postcode is always last

        # Create a dictionary with the extracted details
        if managers_name:
            data = {
                "Manager's Name": managers_name,
                "Company's Name": companys_name,
                "Email": email,
                "Phone Number": phone_number,
                "Postcode": postcode
            }

            if managers_name and managers_name not in [item["Manager's Name"] for item in all_data]:
                all_data.append(data)
    
    return all_data

file_name = "tests/find_adviser/UK postcodes.xlsx"
column_letter = "A"
column_data = extract_column_data(file_name, column_letter)

results = []

# Set up threading to parallelize the process
def worker(postcodes, results):
    for postcode in postcodes:
        data = scrape_data_for_postcode(postcode)
        if data:
            results.extend(data)

# Split the work into chunks for threads
thread_count = 5
chunk_size = len(column_data) // thread_count
threads = []
for i in range(thread_count):
    start_index = i * chunk_size
    end_index = start_index + chunk_size if i != thread_count - 1 else None
    t = threading.Thread(target=worker, args=(column_data[start_index:end_index], results))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

# Save results to JSON
with open('output_list.json', 'w') as file:
    json.dump(results, file, indent=4)




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

def get_lat_lon(postcode, country="UK"):
    geolocator = Nominatim(user_agent="postcode_to_latlon_converter")
    full_address = f"{postcode}, {country}"

    try:
        location = geolocator.geocode(full_address)
        return location.latitude, location.longitude if location else (None, None)
    except GeocoderTimedOut:
        print("Error: geocode failed due to time out")
        return None, None

def extract_column_data(file_name, column_letter, sheet_name=None):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook[sheet_name] if sheet_name else workbook.active
    data = [cell.value for cell in sheet[column_letter] if cell.value is not None]
    workbook.close()
    return data

file_name = "tests/find_adviser/UK postcodes.xlsx"
column_letter = "A"
column_data = extract_column_data(file_name, column_letter)

all_data = []
managers_set = set()


with requests.Session() as session:  # Use a session to reuse connection
    try:
        for cell_value in column_data:
            lat, lon = get_lat_lon(cell_value)
            if not lat or not lon:
                print(f"Could not find coordinates for postcode {cell_value}")
                continue

            data_payload = {
                'advisorLocation': 'Test',
                'lat': lat,
                'lng': lon,
                'withContactDetails': 'on',
                'specialism': 'Investing'
            }

            response = session.post('https://www.thepfs.org/yourmoney/find-an-adviser/', headers=headers, data=data_payload)
            soup = BeautifulSoup(response.content, 'html.parser')

            for li in soup.find_all('li'):
                manager_elem = li.find('h3', class_='adviser-name')
                managers_name = manager_elem.text.strip() if manager_elem else None
                if not managers_name or managers_name in managers_set:
                    continue

                managers_set.add(managers_name)

                email_elem = li.find('div', class_='yui3-u adv-item adv-email')
                email = email_elem.find('a', href=lambda x: x.startswith('mailto:'))['href'].replace('mailto:', '') if email_elem else None
                companys_name = email.split('@')[1].split('.')[0] if email else None

                phone_elem = li.find('div', class_='yui3-u adv-item adv-telephone')
                phone_number = phone_elem.text.strip() if phone_elem else None

                webpage_elem = li.find('div', class_='yui3-u adv-item adv-webpage')
                webpage_url = webpage_elem.text.strip() if webpage_elem else None

                address_elem = li.find('a', class_='showGoogle')
                address_contents = [content.strip() for content in address_elem.stripped_strings] if address_elem else []
                postcode = address_contents[-2] if len(address_contents) > 1 else None

                entry = {
                    "Manager's Name": managers_name,
                    "Company's Name": companys_name,
                    "Email": email,
                    "Webpage": webpage_url,
                    "Phone Number": phone_number,
                    "Postcode": postcode
                }
                all_data.append(entry)

            print('Added',cell_value)

        with open('output_list_full.json', 'w') as file:
            json.dump(all_data, file, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")
        with open('error_output_list_full.json', 'w') as file:
            json.dump(all_data, file, indent=4)
        print("Data saved to 'error_output_list_full.json' due to an exception.")
        raise  # re-raise the exception to see the traceback

    # Save the full results if no exception occurs
    with open('output_list_full.json', 'w') as file:
        json.dump(all_data, file, indent=4)




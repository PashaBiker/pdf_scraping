import json
from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import openpyxl

# Step 1: Create a session object and make an initial request
session = requests.Session()
headers = {
    'authority': 'adviserbook.co.uk',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'client_id=eyJpdiI6Ill5YVRvYStEYTNRd2FnS0ZvNi91emc9PSIsInZhbHVlIjoidGIwQnI2TE5zTjZGR2hHYWpubmhwdGZPRTcvQTFkb1lLUGdoZ09wa0t0YWpCcnkrajcxck9rTmN5RUpiNER6SWZJUzY3QUV5c21YUTBxdU1DRTg3QkE9PSIsIm1hYyI6IjlkYjg5MjE4Yzc3YzUwYmRhZjM2MGVhMDg5YjE5NTBmNTc1ZGNmYmVmNTZhNmRhOTAzNDY5OWM1YTZjYTJmN2YiLCJ0YWciOiIifQ%3D%3D; cookiesAccepted=true; _gid=GA1.3.12789545.1703093485; _gat=1; _gat_gtag_UA_92449015_1=1; _ga=GA1.1.884276600.1703004649; XSRF-TOKEN=eyJpdiI6Im9KQ3ZHS1Y3YmI1NXRDS0NydXQ4VkE9PSIsInZhbHVlIjoiTEFuMTNMMGRtQk9TdmtLNEdwTjRxa3MxbysrWCtwR1FnMjVXd2NiUW1Yd2FMdlIrVzVnSHd6U3V6N0V6SGJEM2pvMW9UeEJEV3lNVDVkblBDcnlHRWZQQWJpTTdpY2ZjQ1dCSWx4Zk04d29lWTEvSzBkTWxXRm5KcW9abTlpSjAiLCJtYWMiOiJjMzA5MDc0NTFiYzhkN2Y4OTMyZmVkZTUxNGUxMWU1YTEwNTA2Yzg0MDNiNGYzYzI2ZjYxOGViYjM2ZTBjZmE5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjVYSzA0dW1USjhkUG1ubzBXelhUdmc9PSIsInZhbHVlIjoic0dZT2x3bVpZamxiV1JqbDBybGRta0JoRzZLSWNGcWFJZFNYNXhicThuUjdFU0dSVlRUNG91VTBaMXkxZTkwN0hWMGNoWmFweXc5NXZlbitHSjJiNVVCMHB5bUszY29Fd2FjVE03WjI1Ym84ZUttUWRXbXROQy95NUtSRzJOMWgiLCJtYWMiOiJkMzhiOGNmN2YxZjQ4Y2U3N2I4ZTZlNDU2ZWVhNzUxMjM0ZGQxM2Y5YTViMWY4YTA0OWY2ZDZiMWFhNzM2NDYwIiwidGFnIjoiIn0%3D; last_query=eyJpdiI6Ikhnd2tVWDV1TG9qQlpFblBXK0xwdWc9PSIsInZhbHVlIjoid2Rub3pBZlpEY3ExSnlhemhWYmpQV25jM1hwQnRQU3lYeGlydVRnYzZoNjFHV3ZVRnRhVlVUMk5zMWdBaHhKbiIsIm1hYyI6IjlhOWMwNzJkYzExYzc3NmJhZTgyZjViZjAwY2Q2ODBhNWE3OTI1N2RiYWE0NjI4YTNhYmZhYmY2OThmOTAyNTgiLCJ0YWciOiIifQ%3D%3D; _ga_YFS57NGF8S=GS1.1.1703202225.7.1.1703202281.4.0.0',
    'origin': 'https://adviserbook.co.uk',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',}

initial_response = session.get('https://adviserbook.co.uk',headers=headers)

soup = BeautifulSoup(initial_response.content, 'html.parser')
meta_tag = soup.find('meta', {'name': 'csrf-token'})
csrf_token = meta_tag['content'] if meta_tag else None

# Check if the CSRF token is retrieved successfully
if not csrf_token:
    raise ValueError("Failed to retrieve CSRF token.")

# Step 2: Extract 'client_id', 'laravel_session', and 'XSRF-TOKEN' from session cookies
client_id = session.cookies.get('client_id')
laravel_session = session.cookies.get('laravel_session')
xsrf_token = session.cookies.get('XSRF-TOKEN')

# Check if the tokens are retrieved successfully
if not all([client_id, laravel_session, xsrf_token]):
    raise ValueError("Failed to retrieve necessary cookies.")

cookies = {
    'client_id': client_id,
    'cookiesAccepted': 'true',
    '_gid': 'GA1.3.12789545.1703093485',
    '_gat': '1',
    '_gat_gtag_UA_92449015_1': '1',
    '_ga': 'GA1.1.884276600.1703004649',
    'XSRF-TOKEN': xsrf_token,
    'laravel_session': laravel_session,
    # 'last_query': 'eyJpdiI6Ikhnd2tVWDV1TG9qQlpFblBXK0xwdWc9PSIsInZhbHVlIjoid2Rub3pBZlpEY3ExSnlhemhWYmpQV25jM1hwQnRQU3lYeGlydVRnYzZoNjFHV3ZVRnRhVlVUMk5zMWdBaHhKbiIsIm1hYyI6IjlhOWMwNzJkYzExYzc3NmJhZTgyZjViZjAwY2Q2ODBhNWE3OTI1N2RiYWE0NjI4YTNhYmZhYmY2OThmOTAyNTgiLCJ0YWciOiIifQ%3D%3D',
    # '_ga_YFS57NGF8S': 'GS1.1.1703202225.7.1.1703202281.4.0.0',
}

# Define headers and JSON data for the POST request
headers = {
    'authority': 'adviserbook.co.uk',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'client_id=eyJpdiI6Ill5YVRvYStEYTNRd2FnS0ZvNi91emc9PSIsInZhbHVlIjoidGIwQnI2TE5zTjZGR2hHYWpubmhwdGZPRTcvQTFkb1lLUGdoZ09wa0t0YWpCcnkrajcxck9rTmN5RUpiNER6SWZJUzY3QUV5c21YUTBxdU1DRTg3QkE9PSIsIm1hYyI6IjlkYjg5MjE4Yzc3YzUwYmRhZjM2MGVhMDg5YjE5NTBmNTc1ZGNmYmVmNTZhNmRhOTAzNDY5OWM1YTZjYTJmN2YiLCJ0YWciOiIifQ%3D%3D; cookiesAccepted=true; _gid=GA1.3.12789545.1703093485; _gat=1; _gat_gtag_UA_92449015_1=1; _ga=GA1.1.884276600.1703004649; XSRF-TOKEN=eyJpdiI6Im9KQ3ZHS1Y3YmI1NXRDS0NydXQ4VkE9PSIsInZhbHVlIjoiTEFuMTNMMGRtQk9TdmtLNEdwTjRxa3MxbysrWCtwR1FnMjVXd2NiUW1Yd2FMdlIrVzVnSHd6U3V6N0V6SGJEM2pvMW9UeEJEV3lNVDVkblBDcnlHRWZQQWJpTTdpY2ZjQ1dCSWx4Zk04d29lWTEvSzBkTWxXRm5KcW9abTlpSjAiLCJtYWMiOiJjMzA5MDc0NTFiYzhkN2Y4OTMyZmVkZTUxNGUxMWU1YTEwNTA2Yzg0MDNiNGYzYzI2ZjYxOGViYjM2ZTBjZmE5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjVYSzA0dW1USjhkUG1ubzBXelhUdmc9PSIsInZhbHVlIjoic0dZT2x3bVpZamxiV1JqbDBybGRta0JoRzZLSWNGcWFJZFNYNXhicThuUjdFU0dSVlRUNG91VTBaMXkxZTkwN0hWMGNoWmFweXc5NXZlbitHSjJiNVVCMHB5bUszY29Fd2FjVE03WjI1Ym84ZUttUWRXbXROQy95NUtSRzJOMWgiLCJtYWMiOiJkMzhiOGNmN2YxZjQ4Y2U3N2I4ZTZlNDU2ZWVhNzUxMjM0ZGQxM2Y5YTViMWY4YTA0OWY2ZDZiMWFhNzM2NDYwIiwidGFnIjoiIn0%3D; last_query=eyJpdiI6Ikhnd2tVWDV1TG9qQlpFblBXK0xwdWc9PSIsInZhbHVlIjoid2Rub3pBZlpEY3ExSnlhemhWYmpQV25jM1hwQnRQU3lYeGlydVRnYzZoNjFHV3ZVRnRhVlVUMk5zMWdBaHhKbiIsIm1hYyI6IjlhOWMwNzJkYzExYzc3NmJhZTgyZjViZjAwY2Q2ODBhNWE3OTI1N2RiYWE0NjI4YTNhYmZhYmY2OThmOTAyNTgiLCJ0YWciOiIifQ%3D%3D; _ga_YFS57NGF8S=GS1.1.1703202225.7.1.1703202281.4.0.0',
    'origin': 'https://adviserbook.co.uk',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-xsrf-token': xsrf_token,
}

def get_lat_lon(postcode, country="UK"):
    geolocator = Nominatim(user_agent="postcode_to_latlon_converter")
    full_address = f"{postcode}, {country}"

    try:
        location = geolocator.geocode(full_address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
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

for cell_value in column_data:
    lat, lon = get_lat_lon(cell_value)

    json_data = {
        'data': {
            'pcds': {
                'longitude': lon,
                'latitude': lat,
            },
            'method': 'postcode',
            'query': 'London',
            'orig_query': 'London',
            'dist': 50,
        },
        '_token': csrf_token,  # Use the extracted XSRF token if needed here
    }


    # Step 3: Make the POST request using the session
    response = session.post('https://adviserbook.co.uk/search/get-results', cookies=cookies, headers=headers, json=json_data)
    print(response.content)
    # print(cookies)

    data = response.json()  # This will give you a Python dictionary

    # Write the JSON data to a file
    print(cell_value)
    with open('tests/a_adviserbook/services.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

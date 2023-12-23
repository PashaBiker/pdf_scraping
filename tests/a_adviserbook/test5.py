import json
import time
import requests

cookies = {
    'client_id': 'eyJpdiI6Ill5YVRvYStEYTNRd2FnS0ZvNi91emc9PSIsInZhbHVlIjoidGIwQnI2TE5zTjZGR2hHYWpubmhwdGZPRTcvQTFkb1lLUGdoZ09wa0t0YWpCcnkrajcxck9rTmN5RUpiNER6SWZJUzY3QUV5c21YUTBxdU1DRTg3QkE9PSIsIm1hYyI6IjlkYjg5MjE4Yzc3YzUwYmRhZjM2MGVhMDg5YjE5NTBmNTc1ZGNmYmVmNTZhNmRhOTAzNDY5OWM1YTZjYTJmN2YiLCJ0YWciOiIifQ%3D%3D',
    'cookiesAccepted': 'true',
    '_gid': 'GA1.3.12789545.1703093485',
    'last_query': 'eyJpdiI6Ikhnd2tVWDV1TG9qQlpFblBXK0xwdWc9PSIsInZhbHVlIjoid2Rub3pBZlpEY3ExSnlhemhWYmpQV25jM1hwQnRQU3lYeGlydVRnYzZoNjFHV3ZVRnRhVlVUMk5zMWdBaHhKbiIsIm1hYyI6IjlhOWMwNzJkYzExYzc3NmJhZTgyZjViZjAwY2Q2ODBhNWE3OTI1N2RiYWE0NjI4YTNhYmZhYmY2OThmOTAyNTgiLCJ0YWciOiIifQ%3D%3D',
    '_ga': 'GA1.3.884276600.1703004649',
    '_gat': '1',
    '_ga_YFS57NGF8S': 'GS1.3.1703270420.8.0.1703270420.60.0.0',
    'XSRF-TOKEN': 'eyJpdiI6IkN5aGg1d3lTWm5BV3lTdWp5OXIzSVE9PSIsInZhbHVlIjoiL3d4YkJ3UGUzMHVNVnpvc0NqSEprZERrYU12RjA5UTJZeUhJSXFHOXJUczkvcXNpYnNFOFVSWlVzTXVsSFVySWFBMXBGUktkeXNya05IQ0swdFAvUUIxaEhXampjREVOamlTU0s2RzQ2cjZEMmJ5Vk05N1RwSTRvdEdFODc5aFQiLCJtYWMiOiJmOGRlYWNjOGM2N2IzODA2MzhiZWM1ZmIzYmIxNjI2YzdhYzUxMzZkYmM2YzQ4NjBlNjg4MWMwODMzZjFlOWJlIiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6IkdLanpqYmYyMlVRRDRtN2RtT0RlZ2c9PSIsInZhbHVlIjoiajJIcU1ySmpCOHVNdWFnVlc0U0lxT1hkUk0wZ3hLb2Q4NzlKSHBkVERSbWtkbkNYSWNGRk9yY0FoaTU0UHMvQStLODN4aFFiVytsZUp1VFlNc3hGS21ldG1TOWxBL0tCNWJrQ2xoRVV1NjcrNW1mdW1oaitYcTVTc2cxamREVFgiLCJtYWMiOiIzNmRkMDcwYjIyYTY0YzNmMjY1ZTczMzBiYjNlNzE0NzhkYjM2OWNkMTUyM2UxZTJjNGZkMzBkOWJkODMzY2I0IiwidGFnIjoiIn0%3D',
}
headers = {
    'authority': 'adviserbook.co.uk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': 'client_id=eyJpdiI6Ill5YVRvYStEYTNRd2FnS0ZvNi91emc9PSIsInZhbHVlIjoidGIwQnI2TE5zTjZGR2hHYWpubmhwdGZPRTcvQTFkb1lLUGdoZ09wa0t0YWpCcnkrajcxck9rTmN5RUpiNER6SWZJUzY3QUV5c21YUTBxdU1DRTg3QkE9PSIsIm1hYyI6IjlkYjg5MjE4Yzc3YzUwYmRhZjM2MGVhMDg5YjE5NTBmNTc1ZGNmYmVmNTZhNmRhOTAzNDY5OWM1YTZjYTJmN2YiLCJ0YWciOiIifQ%3D%3D; cookiesAccepted=true; _gid=GA1.3.12789545.1703093485; last_query=eyJpdiI6Ikhnd2tVWDV1TG9qQlpFblBXK0xwdWc9PSIsInZhbHVlIjoid2Rub3pBZlpEY3ExSnlhemhWYmpQV25jM1hwQnRQU3lYeGlydVRnYzZoNjFHV3ZVRnRhVlVUMk5zMWdBaHhKbiIsIm1hYyI6IjlhOWMwNzJkYzExYzc3NmJhZTgyZjViZjAwY2Q2ODBhNWE3OTI1N2RiYWE0NjI4YTNhYmZhYmY2OThmOTAyNTgiLCJ0YWciOiIifQ%3D%3D; _ga=GA1.3.884276600.1703004649; _ga_YFS57NGF8S=GS1.3.1703270420.8.0.1703270420.60.0.0; XSRF-TOKEN=eyJpdiI6InRSWW92NldScVBjczZsZGptUmRkbWc9PSIsInZhbHVlIjoiSTFSMmNjNWJLYUp3MkU2T3ZnNXZ3alJ0QXFKZ2wzejIvbTNlbFRIUmU3dHA5SmR6ZXB4QVkxWnNJTEtXOE1mOG1pRklRbWZGUHpqSDhiQU1zWW12SzdBZVZwMFo5d05oTVJiZjdDKzJnS3dBMVRmTloyaGFheWpNUEQvOWZwQm0iLCJtYWMiOiJmOWMxZDNlYjZmYmUxMjdhZmY0NWQyODRlZThiMDE4YjhkOTEyNTRkNDI2OWIxN2ExNmMzYmM0Yjc4MTM0MjVlIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6InZvbkNOeEloQUUxVzhtckZCcHRZdlE9PSIsInZhbHVlIjoiWlFqQWhtMkhleW9DQXEwRGFjNFlkRU13enBLQXovaEFoQ3FZbDZPMjBidHNlY2NWMjAxeE5id2lsUmZncVJLK3lPdWtDZHRqZjNNTVhTbmZJdURZbWlTTnFsWHRkOERpMWFTTjhwbkl1a0JJVEI1Wm1qNGpveEppaGpHS25qdXgiLCJtYWMiOiIxNjczMTY3ZjU1NTk0ZDE0NTc0MzVjNGU5OTYwMzNjZmE0ZGIxMTA4OTE4MzdmMWNkOWU5NjAzZjE3YmU0MGQyIiwidGFnIjoiIn0%3D',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

import requests
from bs4 import BeautifulSoup

# List of company data
with open('tests/a_adviserbook/unique_filtered_companies copy 2.json', 'r') as file:
    companies = json.load(file)
    # print("Data loaded from file:", data)  # Diagnostic print


# Base URL for the website
base_url = "https://www.adviserbook.co.uk/financial-advisers/"

for company in companies:
    try:
        office_url = company.get("office_url")
        if office_url:
            # Construct full URL
            full_url = base_url + office_url

            # Send HTTP request
            response = requests.get(full_url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the email address
                email_div = soup.find("div", class_="lb-row tac")
                if email_div:
                    email_tag = email_div.find("a", href=lambda href: href and "mailto:" in href)
                    if email_tag:
                        company['email'] = email_tag.text
                    else:
                        company['email'] = "Not found"
                else:
                    company['email'] = "Not found"
            else:
                company['email'] = "Failed to load page"

        # Wait a bit before the next request
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        company['email'] = "Error"

# Optionally, save the updated companies list to a file
with open('updated_companies.json', 'w') as outfile:
    json.dump(companies, outfile)
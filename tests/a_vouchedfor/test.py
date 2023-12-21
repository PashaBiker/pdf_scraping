import json
import pandas as pd
import requests

headers = {
    'authority': 'sparta.vouchedfor.co.uk',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://www.vouchedfor.co.uk',
    'referer': 'https://www.vouchedfor.co.uk/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'vf-save-logs': 'true',
}

params = {
    'include_travel_professionals': '1',
    'is_contactable': '1',
    'location': 'ze3',
    'latitude': '',
    'longitude': '',
    'search_range': '10000',
    'vertical_id': '5',
    'fn': '',
    'ln': '',
    'advanced_qualifications': '0',
    'fixed_fees': '0',
    'limit': '10000',
    'sort_by': 'sigmoid',
}

response = requests.get('https://sparta.vouchedfor.co.uk/v2', params=params, headers=headers)

print(response.content)
# Преобразование ответа в JSON
data = response.json()

# Сохранение данных в файл
with open('tests/a_vouchedfor/ze3.json', 'w') as file:
    json.dump(data, file, indent=4)


# Extracting the required fields
extracted_data = []
for item in data["data"]:
    extracted_data.append({
        "First Name": item.get("first_name", ""),
        "Title": item.get("title", ""),
        "Last Name": item.get("last_name", ""),
        "Firm Name": item.get("firm_name", ""),
        "Phone Number": item.get("phone_number", ""),
        "Home Town": item.get("home_town", "")
    })

# Convert to DataFrame
df = pd.DataFrame(extracted_data)

# Save to Excel file
df.to_excel("output.xlsx", index=False)


print("Данные сохранены в файл 'ze3.json'.")
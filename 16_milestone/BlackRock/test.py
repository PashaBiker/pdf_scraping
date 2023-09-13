import json
import requests
from requests_html import HTMLSession

headers = {
    'authority': 'www.blackrock.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

session = HTMLSession()

response = session.get('https://www.blackrock.com/uk/individual/products/295873/blackrock-pension-growth-fund', headers=headers)

# Ожидание 4 секунды
response.html.render(sleep=4, timeout=20.0)

# Если вы хотите работать с содержимым ответа
html_content = response.html.html

# print(html_content)

import re

extracted_data = []

for pattern in [r'var tabsAssetclassDataTable =(\[.*?\]);',
                r'var subTabsRegionsDataTable =(\[.*?\]);',
                r'var subTabsCountriesDataTable =(\[.*?\]);']:
    try:
        match = re.search(pattern, html_content).group(1)[1:-1]
        extracted_data.append(match)
    except Exception as e:
        pass

# Соединим все успешно извлеченные данные
combined_data = "[" + ",".join(extracted_data) + "]"
# Fix the JSON format
corrected_json_string = re.sub(r',\s*}', '}', combined_data)

# Parse the corrected JSON string
data = json.loads(corrected_json_string)

# Extract name-value pairs
name_value_pairs = [(entry["name"], entry["value"]) for entry in data]
print(name_value_pairs)
# Print the name and value pairs
# for name, value in name_value_pairs:
    # print(f"{name}:{value}")

# Compute and print the sum
sum_values = sum(float(entry["value"]) for entry in data)
print(f"\nTotal Sum: {sum_values:.2f}")
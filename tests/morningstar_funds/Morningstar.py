import re
import pandas as pd
import requests
import json

def fix_ISIN(data):
    for item in data:
        tenfore_id = item.get("TenforeId", "")
        # Regular expression to remove everything before and including the second dot
        modified_id = re.sub(r'^[^.]*\.[^.]*\.', '', tenfore_id)
        item["TenforeId"] = modified_id
    return data

def edit_currency(data_list):
    for data_item in data_list:
        # Changing "PriceCurrency" from "GBX" to "GBP"
        if data_item.get("PriceCurrency") == "GBX":
            data_item["PriceCurrency"] = "GBP"

        # Dividing "OngoingCostActual" by 100 if it exists
        if "OngoingCostActual" in data_item:
            data_item["OngoingCostActual"] = data_item["OngoingCostActual"] / 100

    return data_list

headers = {
    'authority': 'tools.morningstar.co.uk',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://www.morningstar.co.uk',
    'referer': 'https://www.morningstar.co.uk/uk/screener/fund.aspx',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

def make_request(page_number):
    params = {
        'page': str(page_number),
        'pageSize': '50000',  # Adjusted to the maximum allowed
        'sortOrder': 'LegalName asc',
        'outputType': 'json',
        'version': '1',
        'languageId': 'en-GB',
        'currencyId': 'GBP',
        'universeIds': 'FOGBR$$ALL|FOCHI$$ONS',
        'securityDataPoints': 'LegalName|SecId|PriceCurrency|TenforeId|CategoryName|OngoingCostActual',
        'filters': '',
        'term': '',
        'subUniverseId': '',
    }
    response = requests.get(
        'https://tools.morningstar.co.uk/api/rest.svc/klr5zyak8x/security/screener',
        params=params,
        headers=headers,
    )
    return json.loads(response.content.decode('utf-8'))

# Make requests for both pages
data_page_1 = make_request(1)
data_page_2 = make_request(2)

# Combine the data from both pages
combined_data = data_page_1['rows'] + data_page_2['rows']

modified_data = fix_ISIN(combined_data)
modified_data = edit_currency(modified_data)
# pretty print the JSON data
# print(json.dumps(modified_data, indent=4))
with open('data.json', 'w') as file:
    json.dump(modified_data, file)


# Convert the data into a pandas DataFrame
df = pd.DataFrame(modified_data)

# Rename columns to match the desired Excel headers
df.rename(columns={
    "LegalName": "Name",
    "SecId": "SecID",
    "TenforeId": "ISIN",
    "PriceCurrency": "Currency",
    "CategoryName": "Morningstar Category™",
    "OngoingCostActual": "Ongoing Charge"
}, inplace=True)

# Save the DataFrame to an Excel file
excel_filename = "Morningstar.xlsx"
df.to_excel(excel_filename, index=False)
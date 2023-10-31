import json
import requests

headers = {
    'authority': 'maps.googleapis.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://www.thepfs.org/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-client-data': 'CLO1yQEIiLbJAQijtskBCKmdygEIzeXKAQiUocsBCIWgzQEIucrNARiPzs0BGNXczQE=',
}

response = requests.get(
    'https://maps.googleapis.com/maps/api/place/js/AutocompletionService.GetQueryPredictionsJson?1sZE2&4sru-RU&15e3&21m1&2e1&callback=_xdc_._nz5fd4&client=gme-thecharteredinsurance&token=115306',
    headers=headers,
)

byte_data = response.content

# Step 1: Decode the byte string
decoded_str = byte_data.decode('utf-8')

# Remove any JavaScript callback or function wrapping, assuming it starts with "/**/_xdc_._nz5fd4 && _xdc_._nz5fd4(" and ends with ");"
cleaned_data = decoded_str[decoded_str.index('{'):decoded_str.rindex('}')+1]

# Step 2: Load the JSON data into a Python object
data = json.loads(cleaned_data)

pred = data['predictions']
print(pred[0]['description'])

# Step 3: Extract and work with the desired fields, for demonstration, we'll print the "description" of each prediction
# for prediction in data['predictions']:
#     print(prediction['description'])
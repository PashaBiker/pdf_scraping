import requests

headers = {
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Hash': '389c9181cf50f8e9fbe3575e376e4c46a6045776',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.schroders.com/',
    'Application-Name': 'uk.investment-solutions',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://frontend.schdr.eu-central-1.isgdigital.com/api/fund/SCHDR_F000016OTO/document/?distribution=uk.investment-solutions&endpoint=fis&environment=production&expiration=T09:00&expirationIdentifier=6%2F10%2F2023&installationName=uk.investment-solutions&language=en&publicRules=%7B%22types%22:%5B%22Factsheet%22,%22Factsheet+Monthly%22%5D%7D&sensitivity=confidential',
    headers=headers,
)

print(response.content)

import hashlib

# Предполагаемые данные для хеширования
data = 'F000016OTO'

# Генерация хеша с использованием SHA-1
generated_hash = hashlib.sha1(data.encode()).hexdigest()

# print(generated_hash)
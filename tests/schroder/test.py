import requests

headers = {
    'authority': 'frontend.schdr.eu-central-1.isgdigital.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'application-name': 'uk.investment-solutions',
    'hash': 'e1576ce160f8542fba078dfdb274cb49863aedf0',
    'origin': 'https://www.schroders.com',
    'referer': 'https://www.schroders.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://frontend.schdr.eu-central-1.isgdigital.com/api/fund/SCHDR_F000016P9I/document/?distribution=uk.investment-solutions&endpoint=fis&environment=production&expiration=T09:00&expirationIdentifier=6%2F10%2F2023&installationName=uk.investment-solutions&language=en&publicRules=%7B%22types%22:%5B%22Factsheet%22,%22Factsheet+Monthly%22%5D%7D&sensitivity=confidential',
    headers=headers,
)

print(response.content)
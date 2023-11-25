from bs4 import BeautifulSoup
import requests

cookies = {
    'website#lang': 'en',
    'Language_Cookie': 'en',
    'shell#lang': 'en',
    'ASP.NET_SessionId': 'noxseod2jbwfnxmrcg1mocs1',
    '__RequestVerificationToken': 'xcV0Q2zApTZd8Qa6566tH9zJRkl1_93pXMc-DYaiYg1qI7kXR09UcLH-kt7wZ9TZjEBoVtODLGk-w8yHvlXG0NI2O8WMwnQ5fw2u0j5hd4k1',
    'SC_ANALYTICS_GLOBAL_COOKIE': '24378da28b3645e2851a5123c5b56b74|True',
    'CookieScriptConsent': '{"action":"accept","categories":"[\\"targeting\\",\\"performance\\",\\"functionality\\"]","key":"03d91887-b3e1-45f1-a36c-b39b3a3b649f"}',
    '_ga': 'GA1.1.1569645226.1700899837',
    'cusid': '1700899837545',
    'cusid': '1700899837545',
    'cuvid': 'c19b1213076c4e7bb1ea609d819eebfc',
    'Cookie_Expiry': '2024-11-24',
    'Shared_User_Details_Cookie': 'gb,1,FinancialIntermediary',
    '.AspNet.Cookies': 'Tg80kynUR5n8zYHzJyO37LDKpzKXtoJ2bLHpaETH2xmtsmkN_-DoLtYGJWH67HWWKED6z5-QRkavJKZ4aBr5l1MtMbEaFN1zrMcvg_BKjDE_7dnGUdBBrpSmFzIFVwXXbHEKr59d339AaEmE-gY5Yg3RXhDxt0ZJ0rNMSjw9d0vsYhIu1aJQ1Nz1fSrZlaQeikoVTKvghlyulaXQ7jW7Z3L7hle_Vl4UxNQO6yGkLVckZqZTBdd7IVfHraGtN9XmrstoazPk3e0Zl0dxwkQ5Ntc0WrkBVIlhClJHC96CcLrBVMLYCzKp9E01uTksxNyiG8HfLeE_KAeplBpILdaeOgu4D69tjTsZ3ubjZeGazoHjQg8kfULeB0Umx4W9KfWoORtCw7eVYJ-bGWwvmqhORdJk0SUinOy44D0S3pr1fyDVbDZOGNDG1itmIhMI534c',
    '_ga_X1YCE0Q8FZ': 'GS1.1.1700899837.1.1.1700899851.0.0.0',
    'cuvon': '1700899851269',
}

headers = {
    'authority': 'www.gam.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9',
    # 'cookie': 'website#lang=en; Language_Cookie=en; shell#lang=en; ASP.NET_SessionId=noxseod2jbwfnxmrcg1mocs1; __RequestVerificationToken=xcV0Q2zApTZd8Qa6566tH9zJRkl1_93pXMc-DYaiYg1qI7kXR09UcLH-kt7wZ9TZjEBoVtODLGk-w8yHvlXG0NI2O8WMwnQ5fw2u0j5hd4k1; SC_ANALYTICS_GLOBAL_COOKIE=24378da28b3645e2851a5123c5b56b74|True; CookieScriptConsent={"action":"accept","categories":"[\\"targeting\\",\\"performance\\",\\"functionality\\"]","key":"03d91887-b3e1-45f1-a36c-b39b3a3b649f"}; _ga=GA1.1.1569645226.1700899837; cusid=1700899837545; cusid=1700899837545; cuvid=c19b1213076c4e7bb1ea609d819eebfc; Cookie_Expiry=2024-11-24; Shared_User_Details_Cookie=gb,1,FinancialIntermediary; .AspNet.Cookies=Tg80kynUR5n8zYHzJyO37LDKpzKXtoJ2bLHpaETH2xmtsmkN_-DoLtYGJWH67HWWKED6z5-QRkavJKZ4aBr5l1MtMbEaFN1zrMcvg_BKjDE_7dnGUdBBrpSmFzIFVwXXbHEKr59d339AaEmE-gY5Yg3RXhDxt0ZJ0rNMSjw9d0vsYhIu1aJQ1Nz1fSrZlaQeikoVTKvghlyulaXQ7jW7Z3L7hle_Vl4UxNQO6yGkLVckZqZTBdd7IVfHraGtN9XmrstoazPk3e0Zl0dxwkQ5Ntc0WrkBVIlhClJHC96CcLrBVMLYCzKp9E01uTksxNyiG8HfLeE_KAeplBpILdaeOgu4D69tjTsZ3ubjZeGazoHjQg8kfULeB0Umx4W9KfWoORtCw7eVYJ-bGWwvmqhORdJk0SUinOy44D0S3pr1fyDVbDZOGNDG1itmIhMI534c; _ga_X1YCE0Q8FZ=GS1.1.1700899837.1.1.1700899851.0.0.0; cuvon=1700899851269',
    'referer': 'https://www.gam.com/en/funds/featured-funds/managed-fund-solutions',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'isFundList': 'True',
    'filterId': 'c09a43b7-60a4-49b0-89eb-9dbece288789',
    '_': '1700899851163',
}

response = requests.get('https://www.gam.com/api/sitecore/FundList/GetFunds', 
                        params=params, 
                        # cookies=cookies, 
                        headers=headers)

html = response.content

print(html)

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Initialize an empty dictionary to store the results
funds_dict = {}

# Iterate through each row in the table
for row in soup.find_all("tr"):
    fund_name_span = row.find("span", {"data-bind": "text: FundName"})
    if fund_name_span:
        fund_name = fund_name_span.get_text()

        # Find the associated link for the English document
        doc_link = row.find("a", href=True, text="EN", attrs={"data-ga-action": "Document"})
        if doc_link:
            funds_dict[fund_name] = doc_link.get('href')

# Print the results
print(funds_dict)
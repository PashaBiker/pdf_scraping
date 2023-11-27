from bs4 import BeautifulSoup
import requests
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
    'cuvid': 'c19b1213076c4e7bb1ea609d819eebfc',
    'Cookie_Expiry': '2024-11-24',
    'Shared_User_Details_Cookie': 'gb,1,FinancialIntermediary',
    '.AspNet.Cookies': 'UItVdqxiBWOg7vmKD9kkqleevntp3qDr2nRC9Rxdg22HH4Fs5N7QPVIm5it9ckZsx2knagqfvzftfxBmvnvPcHzjsVp8jn5CqrXhhWeNz78y2iKRTgMD_aHJmVR1KXiGjifFckno84KjuM4TTkBiRDqbNHy53BBzu_7o13dmCbTzbThd5NiaLQ9zEgn8c4cNBm7PqvnxdgSGGNPNgl5nj_A3CAUU28qccjwChXRQWQn8rJdRdgsaWXTqkxh1xgg1tgydzBo1kZ2-NJ0YL7aXVk4b7_tCD3DLL8k3R35pUtEMtaip6EjwHqp7msGBZ0xQhJEb2VtFk0msDsid5EI3DvOIf6AcNx2r68RdaKndjp4z_zbmN5Nb_w_ig0_SxSgNnzrW_z27my1s1gKF-IIMpXTeIJYoZvc2UOZprO2VzA3rgJxKQuHRmjIheYV9l84e',
    '_ga_X1YCE0Q8FZ': 'GS1.1.1700928541.2.0.1700928541.0.0.0',
}

headers = {
    'authority': 'www.gam.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9',
    # 'cookie': 'website#lang=en; Language_Cookie=en; shell#lang=en; ASP.NET_SessionId=noxseod2jbwfnxmrcg1mocs1; __RequestVerificationToken=xcV0Q2zApTZd8Qa6566tH9zJRkl1_93pXMc-DYaiYg1qI7kXR09UcLH-kt7wZ9TZjEBoVtODLGk-w8yHvlXG0NI2O8WMwnQ5fw2u0j5hd4k1; SC_ANALYTICS_GLOBAL_COOKIE=24378da28b3645e2851a5123c5b56b74|True; CookieScriptConsent={"action":"accept","categories":"[\\"targeting\\",\\"performance\\",\\"functionality\\"]","key":"03d91887-b3e1-45f1-a36c-b39b3a3b649f"}; _ga=GA1.1.1569645226.1700899837; cuvid=c19b1213076c4e7bb1ea609d819eebfc; Cookie_Expiry=2024-11-24; Shared_User_Details_Cookie=gb,1,FinancialIntermediary; .AspNet.Cookies=UItVdqxiBWOg7vmKD9kkqleevntp3qDr2nRC9Rxdg22HH4Fs5N7QPVIm5it9ckZsx2knagqfvzftfxBmvnvPcHzjsVp8jn5CqrXhhWeNz78y2iKRTgMD_aHJmVR1KXiGjifFckno84KjuM4TTkBiRDqbNHy53BBzu_7o13dmCbTzbThd5NiaLQ9zEgn8c4cNBm7PqvnxdgSGGNPNgl5nj_A3CAUU28qccjwChXRQWQn8rJdRdgsaWXTqkxh1xgg1tgydzBo1kZ2-NJ0YL7aXVk4b7_tCD3DLL8k3R35pUtEMtaip6EjwHqp7msGBZ0xQhJEb2VtFk0msDsid5EI3DvOIf6AcNx2r68RdaKndjp4z_zbmN5Nb_w_ig0_SxSgNnzrW_z27my1s1gKF-IIMpXTeIJYoZvc2UOZprO2VzA3rgJxKQuHRmjIheYV9l84e; _ga_X1YCE0Q8FZ=GS1.1.1700928541.2.0.1700928541.0.0.0',
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
    'cache': 'b3771af6-92d9-44a7-ab4f-84606d84e685',
    '_': '1700928541824',
}

response = requests.get('https://www.gam.com/api/sitecore/FundList/GetFunds', params=params, #cookies=cookies,
                         headers=headers)

initial_response = requests.get('https://www.gam.com/api/sitecore/FundList/GetFunds')
cookies = initial_response.cookies
print(cookies)
response = requests.get('https://www.gam.com/api/sitecore/FundList/GetFunds', params=params, cookies=cookies, headers=headers)


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
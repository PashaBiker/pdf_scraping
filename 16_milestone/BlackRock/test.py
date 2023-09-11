import json
import requests

cookies = {
    'ts-uk-one-locale': 'en_GB',
    'blkUserType-uk-one': 'individual',
    'StatisticalAnalyticsEnabled': 'false',
    'OptanonAlertBoxClosed': '2023-09-08T21:48:15.775Z',
    '_gcl_au': '1.1.2132281775.1694209696',
    's_ecid': 'MCMID%7C68686600870714387230605552243712585400',
    '_cs_c': '1',
    'aam_uuid': '68716651610374331820605791830700085349',
    'ELOQUA': 'GUID=746E306AF49F4AE3900E2BE469DC1A07',
    'QSI_SI_cZp9V9dfnRdnGTz_intercept': 'true',
    'AllowAnalytics': 'true',
    'AMCVS_631FF31455E575197F000101%40AdobeOrg': '1',
    '_cs_cvars': '%7B%7D',
    's_cc': 'true',
    'ln_or': 'eyIyNzUxNTM4IjoiZCJ9',
    'uk-one-recent-funds': '319696+230044',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Sep+10+2023+22%3A26%3A36+GMT%2B0300+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=b3e606db-3cc8-4c16-b5a0-9d34d3dc23c5&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0011%3A1&geolocation=UA%3B68&AwaitingReconsent=false',
    'AMCV_631FF31455E575197F000101%40AdobeOrg': '-1303530583%7CMCIDTS%7C19611%7CMCMID%7C68686600870714387230605552243712585400%7CMCAAMLH-1694978797%7C6%7CMCAAMB-1694978797%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1694381197s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0',
    's_sq': '%5B%5BB%5D%5D',
    'omni_newRepeat': '1694374135238-Repeat',
    'utag_main': 'v_id:018a76c4597b0013392c58dd02cd0506f006606700bd0$_sn:6$_se:49$_ss:0$_st:1694375935232$vapi_domain:blackrock.com$_prevpage:uk-one%7Cgb%7Cfund%7Cmymap%204%20select%20income%20fund%20d%20acc%20gbp%3Bexp-1694377735239$ses_id:1694373372857%3Bexp-session$_pn:2%3Bexp-session',
    's_tp': '10706',
    's_ppv': 'uk-one%257Cgb%257Cfund%257Cmymap%25204%2520select%2520income%2520fund%2520d%2520acc%2520gbp%2C100%2C67%2C10706',
    '_cs_id': '166cc2d9-db79-a903-9613-1783fbcfe1d8.1694209696.9.1694417086.1694417086.1621334332.1728373696730',
    '_cs_s': '1.0.0.1694418887135',
    'SSESSIONID_uk-retail01': 'Y2EwZGQzNTAtODNjZC00ZmM5LThlYzktN2FiNGY2YTk3MzU2',
    'STICKY_SESSION_COOKIE_UK_RETAIL01_LIVE': '"ba565fa3eaaab3cd"',
    '_abck': '031E943005C4BB1ABC59191328045A6D~0~YAAQL2ReaHEvY02KAQAArqsrgwr7sTyxJRkZP8MonBvRvVD7NSDlB6DhNB/ZO7gUCGlJfiRUiVquEFqoT8yoA3zj9aKlvegxtAZj9d0atdNpSoiED6QTMxva6X3clT5rafxmLdyw/sLfqyA3IE8VD2+nbjvb2z9jeRW9kQQn3buLTk7meSZ2F3JGm8J9g0QZZ5Rq9DipwA0bvctLXTwW4dm7Ih1dOXr3wfUfADdphtYID3bCMjRuWfnEEvmf9E9lpafYp9fWMNVN6WX5gTCBiLqt0x0z99NrM8iwNPRULWYpFxNYOZN8wgErVqbWmMd+KdZbLRR9hXkk7+5GPdFkvY50OPs3QnpRvgtL+cyIqeyO3WFF+9lrTHy1QCgVJn/osw==~-1~-1~-1',
}

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



from requests_html import HTMLSession

session = HTMLSession()

response = session.get('https://www.blackrock.com/uk/individual/products/319696/mymap-4-select-income-fund/', headers=headers)

# Ожидание 4 секунды
response.html.render(sleep=4, timeout=20.0)

# Если вы хотите работать с содержимым ответа
html_content = response.html.html

# print(html_content)

import re

tabsAssetclassDataTable = re.search(r'var tabsAssetclassDataTable =(\[.*?\]);', html_content)
subTabsCountriesDataTable = re.search(r'var subTabsCountriesDataTable =(\[.*?\]);', html_content) 
subTabsRegionsDataTable = re.search(r'var subTabsRegionsDataTable =(\[.*?\]);', html_content)

tabsAssetclassDataTable_data = tabsAssetclassDataTable.group(1)
subTabsCountriesDataTable_data = subTabsCountriesDataTable.group(1)
subTabsRegionsDataTable_data = subTabsRegionsDataTable.group(1)

combined_list = tabsAssetclassDataTable_data + subTabsCountriesDataTable_data + subTabsRegionsDataTable_data

print(combined_list)

breakpoint()

corrected_json_string = re.sub(r',\s*}', '}', combined_list) # combined_list need to be перероблений

# Now, you can parse the corrected JSON string
data = json.loads(corrected_json_string)
name_value_pairs = [(entry["name"], entry["value"]) for entry in data]

# Вывод пар name и value
for name, value in name_value_pairs:
    print(f"Name: {name}, Value: {value}")

# Вычисление и вывод суммы
sum_values = sum(float(entry["value"]) for entry in data)
print(f"\nTotal Sum: {sum_values:.2f}")

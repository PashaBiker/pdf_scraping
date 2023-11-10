import requests

cookies = {
    'cookies': 'true',
    'RT_uk_LANG': 'en-GB',
    'ad-profile': '%7B%22NeedRefresh%22%3Afalse%2C%22UserType%22%3A0%2C%22AudienceType%22%3A-1%2C%22PortofolioCreated%22%3A0%2C%22IsForObsr%22%3Afalse%2C%22NeedPopupAudienceBackfill%22%3Afalse%2C%22EnableInvestmentInUK%22%3A-1%7D',
    'OptanonAlertBoxClosed': '2023-10-23T14:09:46.095Z',
    '__utma': '192614060.2041555357.1698070168.1698074216.1699618507.3',
    '__utmc': '192614060',
    '__utmz': '192614060.1699618507.3.3.utmcsr=upwork.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    '_gid': 'GA1.3.1863671783.1699618508',
    'ASP.NET_SessionId': '5slvisfhm30tuzqw3l00wxit',
    '__utmt': '1',
    '_ga_8R1W3TJHY4': 'GS1.1.1699618506.3.1.1699619464.0.0.0',
    '_ga_1E5VHFNL9Z': 'GS1.1.1699618506.3.1.1699619464.0.0.0',
    '__utmb': '192614060.5.10.1699618507',
    'AWSALB': 'LoJ6WDSUxb2+Dn416Qa5W2rhqMKBROHTQBK8qCv0RvUfCM0VPhLF2IaQQSMYpTsT7dqmbOEc0M6WLq3QNO6i3FIgiI9SRh+dp3bdYd9ooNcRlcWQfPb/d/1+iCPS',
    'AWSALBCORS': 'LoJ6WDSUxb2+Dn416Qa5W2rhqMKBROHTQBK8qCv0RvUfCM0VPhLF2IaQQSMYpTsT7dqmbOEc0M6WLq3QNO6i3FIgiI9SRh+dp3bdYd9ooNcRlcWQfPb/d/1+iCPS',
    '_ga': 'GA1.3.819309748.1698070168',
    '_gat_gtmLocal': '1',
    '_gat_gtmIntl': '1',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Nov+10+2023+14%3A31%3A05+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.27.0&isIABGlobal=false&hosts=&consentId=a45a069a-1ca3-43a3-a11a-3ec51afea125&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false',
}

headers = {
    'authority': 'www.morningstar.co.uk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'cookies=true; RT_uk_LANG=en-GB; ad-profile=%7B%22NeedRefresh%22%3Afalse%2C%22UserType%22%3A0%2C%22AudienceType%22%3A-1%2C%22PortofolioCreated%22%3A0%2C%22IsForObsr%22%3Afalse%2C%22NeedPopupAudienceBackfill%22%3Afalse%2C%22EnableInvestmentInUK%22%3A-1%7D; OptanonAlertBoxClosed=2023-10-23T14:09:46.095Z; __utma=192614060.2041555357.1698070168.1698074216.1699618507.3; __utmc=192614060; __utmz=192614060.1699618507.3.3.utmcsr=upwork.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _gid=GA1.3.1863671783.1699618508; ASP.NET_SessionId=5slvisfhm30tuzqw3l00wxit; __utmt=1; _ga_8R1W3TJHY4=GS1.1.1699618506.3.1.1699619464.0.0.0; _ga_1E5VHFNL9Z=GS1.1.1699618506.3.1.1699619464.0.0.0; __utmb=192614060.5.10.1699618507; AWSALB=LoJ6WDSUxb2+Dn416Qa5W2rhqMKBROHTQBK8qCv0RvUfCM0VPhLF2IaQQSMYpTsT7dqmbOEc0M6WLq3QNO6i3FIgiI9SRh+dp3bdYd9ooNcRlcWQfPb/d/1+iCPS; AWSALBCORS=LoJ6WDSUxb2+Dn416Qa5W2rhqMKBROHTQBK8qCv0RvUfCM0VPhLF2IaQQSMYpTsT7dqmbOEc0M6WLq3QNO6i3FIgiI9SRh+dp3bdYd9ooNcRlcWQfPb/d/1+iCPS; _ga=GA1.3.819309748.1698070168; _gat_gtmLocal=1; _gat_gtmIntl=1; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Nov+10+2023+14%3A31%3A05+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.27.0&isIABGlobal=false&hosts=&consentId=a45a069a-1ca3-43a3-a11a-3ec51afea125&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

params = {
    'id': 'F00000YC76',
}

response = requests.get(
    'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx',
    params=params,
    # cookies=cookies,
    headers=headers,
)

print(response.content)
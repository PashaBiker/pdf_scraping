import requests
import json

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

params = {
    'page': '1',
    'pageSize': '10',
    'sortOrder': 'LegalName asc',
    'outputType': 'json',
    'version': '1',
    'languageId': 'en-GB',
    'currencyId': 'GBP',
    'universeIds': 'FOGBR$$ALL|FOCHI$$ONS',
    'securityDataPoints': 'SecId|Name|PriceCurrency|TenforeId|LegalName|ClosePrice|Yield_M12|CategoryName|Medalist_RatingNumber|StarRatingM255|SustainabilityRank|GBRReturnD1|GBRReturnW1|GBRReturnM1|GBRReturnM3|GBRReturnM6|GBRReturnM0|GBRReturnM12|GBRReturnM36|GBRReturnM60|GBRReturnM120|MaxFrontEndLoad|OngoingCostActual|PerformanceFeeActual|TransactionFeeActual|MaximumExitCostAcquired|FeeLevel|ManagerTenure|MaxDeferredLoad|InitialPurchase|FundTNAV|EquityStyleBox|BondStyleBox|AverageMarketCapital|AverageCreditQualityCode|EffectiveDuration|MorningstarRiskM255|AlphaM36|BetaM36|R2M36|StandardDeviationM36|SharpeM36|InvestorTypeRetail|InvestorTypeProfessional|InvestorTypeEligibleCounterparty|ExpertiseBasic|ExpertiseAdvanced|ExpertiseInformed|ReturnProfilePreservation|ReturnProfileGrowth|ReturnProfileIncome|ReturnProfileHedging|ReturnProfileOther|TrackRecordExtension',
    'filters': '',
    'term': '',
    'subUniverseId': '',
}

response = requests.get(
    'https://tools.morningstar.co.uk/api/rest.svc/klr5zyak8x/security/screener',
    params=params,
    headers=headers,
)


# convert bytes to string and then load it as JSON
data = json.loads(response.content.decode('utf-8'))

# pretty print the JSON data
print(json.dumps(data, indent=4))
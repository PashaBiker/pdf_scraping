import json
import requests


headers = {
    'authority': 'www.unbiased.co.uk',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    # 'cookie': '_gcl_au=1.1.1579143240.1702892939; _wt.mode-1992134=WT3p6nmmtxGBD8~; _gid=GA1.3.2010802585.1702892940; _hjHasCachedUserAttributes=true; _clck=sypd9m%7C2%7Cfhn%7C0%7C1447; hubspotutk=99b5cb6483bae40cc5cdf16b42799cbf; __hssrc=1; cookiefirst-consent=%7B%22necessary%22%3Atrue%2C%22performance%22%3Atrue%2C%22functional%22%3Atrue%2C%22advertising%22%3Atrue%2C%22timestamp%22%3A1702893387%2C%22type%22%3A%22category%22%2C%22version%22%3A%229a74d43c-9157-4f83-99ad-25d83e2ed6f9%22%7D; _hjSessionUser_754134=eyJpZCI6Ijc2ZDM1YzQ3LWEzZTItNWEzYy05NmE1LWQ2MGQ0YjA1NmE1MSIsImNyZWF0ZWQiOjE3MDI4OTI5NDA1ODQsImV4aXN0aW5nIjp0cnVlfQ==; _wt.cp.previousConv=N%2FA; _hjIncludedInSessionSample_754134=0; _hjSession_754134=eyJpZCI6ImU5OGFhYWUwLTY1YmUtNDZjMC04MmI2LWZmM2Y5MzViMjEzNSIsImMiOjE3MDI5MDYyMTA1OTQsInMiOjAsInIiOjAsInNiIjowfQ==; _hjAbsoluteSessionInProgress=1; __hstc=106493788.99b5cb6483bae40cc5cdf16b42799cbf.1702892943896.1702892943896.1702906211025.2; _gat_UA-10571621-9=1; _gat=1; _ga_Q2N5W5958L=GS1.1.1702906210.2.1.1702906716.59.0.0; _ga=GA1.1.775451887.1702892940; sailthru_pageviews=5; _uetsid=ab9630f09d8a11ee8203e3711979066b; _uetvid=ab96ec709d8a11eea33ed1722dbd0054; _wt.user-1992134=WT37Il7KHgE6cGrckxe6ZnlNXG6Z7BiQRWY1Ew9K_PzL6p2zWTIfD4zELoiO8yUfEkbclh3ZTniIzx3x2WELcRhjRbDXmi9kDjdiSXDMnsFQzH3Rv0rVis79e1swlAf7lid3O3EK5fK_-DvZjbNm-NNmQ8o__lAhWQoPr5Bb6PT3resBvs15RfArqIN1agva_DQqSsaV1DwjGyjAGNPlrQwFCnV_yI~; _wt.control-1992134-ta_57FIFABaseline=WT3SiPP-qE4Uu4In_DNbsnUTBLO7JK_xElvHV-47QC3mvAknxKxGWqr07zdgTvQCqlPcai8UcF64az8ftZ9RSitmSzPlCc4qrRUiPe85kg4-ZX_mWTHaHWgTLhBX-jY9FW1mo1wbHHIclj2QesyckkGAuk1UEgVVv4LF7dxVJUaXgF928qJAhpYKUeBW420A3MSd84WpzQQUsOy94p1yuutPQNFPRJPf6N3TIJsrP3g5zqUxTmy_DCv4-5W8tXpl4NnvoRnssOPlFTQYALJ43RzYA~~; _wt.seenTests=%7B%22ta_57FIFABaseline%22%3A%7B%22expID%22%3A2332678%2C%22timestamp%22%3A1702906716955%7D%2C%22ta_83DirectoryBaseline%22%3A%7B%22expID%22%3A2465049%2C%22timestamp%22%3A1702906716962%7D%7D; _wt.control-1992134-ta_83DirectoryBaseline=WT3rbb5FgtW1vWv3c_7E3mzEnuQVEZhKXBe7Y464HEEmMnsg-YYbyAke3Py8yMvsb7BFLRuanUIHHr0bsz-6SKemgccoIZOuoL6q5SPt34Av_9kz3ze0tYvdk43GTS9A_q0k8fwheovjyrkHbvOs1eQzAdP4HuOapcdWv99uzOXHrFqI5tXj0n_eMxAznSLp7XLizBD_2tTbUu2lSuP3fx0p9y6913HE_T6FhiA3byg1w7Y91nkER5x2OyeUHX59dK9h-7SnHOCeJRkcrBbT5j8iA~~; __hssc=106493788.5.1702906211025; sailthru_visitor=86fb3f93-c787-43a8-bb0c-8162108329b9; _clsk=hm1j62%7C1702906717269%7C8%7C1%7Cw.clarity.ms%2Fcollect',
    'origin': 'https://www.unbiased.co.uk',
    'referer': 'https://www.unbiased.co.uk/profile/financial-adviser/the-private-office-706871',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'Advisers',
    'variables': {
        'id': '706871',
        'limit': 900,
    },
    'query': 'query Advisers($id: ID!, $page: Int, $limit: Int) {\n  profile(id: $id) {\n    id\n    advisers(page: $page, limit: $limit) {\n      items {\n        ... on Adviser {\n          id\n          logo\n          surname\n          job\n          name\n          title\n          suffix\n          accreditations\n          qualifications {\n            ... on Qualification {\n              qualification\n              tooltip\n              __typename\n            }\n            __typename\n          }\n          letters\n          awards\n          languages\n          __typename\n        }\n        __typename\n      }\n      page\n      totalPages\n      total\n      perPage\n      __typename\n    }\n    __typename\n  }\n}\n',
}

response = requests.post('https://www.unbiased.co.uk/directory-api/graphql', headers=headers, json=json_data)
# print(response.content)

html=response.content

string_content = html.decode('utf-8')

# Convert string to JSON
json_data = json.loads(string_content)

# print(json_data)
advisers_info = json_data['data']['profile']['advisers']['items']

# Formatting the required information
formatted_output = []
for adviser in advisers_info:
    title = adviser.get('title', '')
    name = adviser.get('name', '')
    surname = adviser.get('surname', '')
    job = adviser.get('job', '')
    qualifications = ", ".join([q['qualification'] for q in adviser.get('qualifications', [])])
    
    formatted_info = f"{title} {name} {surname} | {job} | {qualifications}"
    formatted_output.append(formatted_info)



print(formatted_output)
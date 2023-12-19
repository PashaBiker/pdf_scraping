import json
import re
from bs4 import BeautifulSoup
import requests

def get_url_id(postcode):

    headers = {
        'authority': 'www.unbiased.co.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_wt.mode-1992134=WT3p6nmmtxGBD8~; _gid=GA1.3.1767446739.1702831025; _gcl_au=1.1.139496384.1702831025; _clck=ue3sqd%7C2%7Cfhm%7C0%7C1446; _hjHasCachedUserAttributes=true; hubspotutk=41edd103bd47560bea1a15e2e352f934; __hssrc=1; _hjSessionUser_754134=eyJpZCI6IjIxODhkYmQxLTIwNjAtNWE4OS1iNjA3LTkyOGNjMDg5OTQyZSIsImNyZWF0ZWQiOjE3MDI4MzEwMjUzMjEsImV4aXN0aW5nIjp0cnVlfQ==; cookiefirst-consent=%7B%22necessary%22%3Atrue%2C%22performance%22%3Atrue%2C%22functional%22%3Atrue%2C%22advertising%22%3Atrue%2C%22timestamp%22%3A1702836790%2C%22type%22%3A%22category%22%2C%22version%22%3A%229a74d43c-9157-4f83-99ad-25d83e2ed6f9%22%7D; _hjSession_754134=eyJpZCI6ImM4NTkzOTAzLWVjNmUtNGQ0MC04Y2FjLTBkY2U4YzZjODIxNCIsImMiOjE3MDI4NDc1ODYzMDEsInMiOjAsInIiOjAsInNiIjowfQ==; _hjAbsoluteSessionInProgress=0; _wt.cp.previousConv=Page_Directory_Adviser_List; _hjIncludedInSessionSample_754134=1; __hstc=106493788.41edd103bd47560bea1a15e2e352f934.1702831025540.1702836782577.1702848036098.3; _ga=GA1.3.1537947773.1702831025; _wt.user-1992134=WT3tZNu8UyvrgoTVv27vMmXNI0zzuwcqrZCbR2R_5Qky2jiV_S2GGJfLx_I_DjsKe5NTnHT5_l-jHP894dRVj3OhoHy8YcJGDT_NYyPMG7dr-uzexyEJ67-GO1yxVIzWxq3D44G60EX3fgdodf796FPdTtH_lCBCqvs6BDVhJhf1O1SfoYHUJuK2fUXMoxnys1Z6LZUGg5CDIQKOf8IFGCSQT9ZKNI~; _wt.control-1992134-ta_83DirectoryBaseline=WT3rbb5FgtW1vWv3c_7E3mzEnuQVEZhKXBe7Y464HEEmMnsg-YYbyAke3Py8yMvsb7BFLRuanUIHHr0bsz-6SKemgccoIZOuoL6q5SPt34Av_9kz3ze0tYvdk43GTS9A_q0k8fwheovjyrkHbvOs1eQzAdP4HuOapcdWv99uzOXHrFqI5tXj0n_eMxAznSLp7XLizBD_2tTbUu2lSuP3fx0p9y6913HE_T6FhiA3byg1w7Y91nkER5x2OyeUHX59dK9h-7SnHOCeJRkcrBbT5j8iA~~; _uetsid=832b63409cfa11eeb77141b02bf5f8d2; _uetvid=832b67409cfa11eeb806713b5214c9dc; sailthru_pageviews=2; _wt.seenTests=%7B%22ta_57FIFABaseline%22%3A%7B%22expID%22%3A2332678%2C%22timestamp%22%3A1702848045177%7D%2C%22ta_83DirectoryBaseline%22%3A%7B%22expID%22%3A2465049%2C%22timestamp%22%3A1702848044716%7D%7D; _wt.control-1992134-ta_57FIFABaseline=WT3SiPP-qE4Uu4In_DNbsnUTBLO7JK_xElvHV-47QC3mvAknxKxGWqr07zdgTvQCqlPcai8UcF64az8ftZ9RSitmSzPlCc4qrRUiPe85kg4-ZX_mWTHaHWgTLhBX-jY9FW1mo1wbHHIclj2QesyckkGAuk1UEgVVv4LF7dxVJUaXgF928qJAhpYKUeBW420A3MSd84WpzQQUsOy94p1yuutPQNFPRJPf6N3TIJsrP3g5zqUxTmy_DCv4-5W8tXpl4NnvoRnssOPlFTQYALJ43RzYA~~; __hssc=106493788.2.1702848036098; sailthru_visitor=23e36438-cf73-48e5-9be0-96826ab42308; _clsk=mh33pm%7C1702848045641%7C6%7C1%7Cy.clarity.ms%2Fcollect; _ga_Q2N5W5958L=GS1.1.1702847587.3.1.1702848045.22.0.0',
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

    response = requests.get(
        f'https://www.unbiased.co.uk/advisers/financial-adviser?adviceArea=Investments&secondaryAdviceArea&search={postcode}&assetValue=£101,000%2B',
        headers=headers,
    )

    # print(response.content)
    html_сontent = response.content

    soup = BeautifulSoup(html_сontent, 'html.parser')

    script_tag = soup.find('script', string=re.compile('__NUXT__'))

    # Extract the JavaScript object
    script_content = script_tag.string

    # file_name = "extracted_script.html"  # You can change the file name as needed
    # with open(file_name, 'w', encoding='utf-8') as file:
    #     file.write(script_content)

    profile_slugs = re.findall(r'profileSlug:\s*"([^"]+)"', script_content)
    last_numbers = [slug.split("-")[-1] for slug in profile_slugs]

    # for url_part, id in zip(profile_slugs, last_numbers):
    #     url = f'https://www.unbiased.co.uk/profile/financial-adviser/{url_part}'
    #     print(url)
    #     print(id)

    json_data = [
        {"url": f"https://www.unbiased.co.uk/profile/financial-adviser/{url_part}", "id": id}
        for url_part, id in zip(profile_slugs, last_numbers)
    ]

    # Convert the Python object to a JSON formatted string
    json_output = json.dumps(json_data, indent=4)

    return json_output


def get_managers_info(id):
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
            'id': id,
            'limit': 900,
        },
        'query': 'query Advisers($id: ID!, $page: Int, $limit: Int) {\n  profile(id: $id) {\n    id\n    advisers(page: $page, limit: $limit) {\n      items {\n        ... on Adviser {\n          id\n          logo\n          surname\n          job\n          name\n          title\n          suffix\n          accreditations\n          qualifications {\n            ... on Qualification {\n              qualification\n              tooltip\n              __typename\n            }\n            __typename\n          }\n          letters\n          awards\n          languages\n          __typename\n        }\n        __typename\n      }\n      page\n      totalPages\n      total\n      perPage\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    Advisers_response = requests.post('https://www.unbiased.co.uk/directory-api/graphql', headers=headers, json=json_data)

    json_data = {
        'operationName': 'Profile',
        'variables': {
            'id': id,
        },
        'query': 'query Profile($id: ID!) {\n  profile(id: $id) {\n    ...profile\n    __typename\n  }\n}\n\nfragment profile on Profile {\n  id\n  address\n  adviceMethods\n  awardWinnerBadge {\n    ...awardWinnerBadge\n    __typename\n  }\n  blog\n  branchLogoPath\n  clientsHelpedCount\n  companyName\n  compliance\n  curn\n  description\n  distance\n  facebook\n  fsaLastCheck\n  advisers {\n    items {\n      ... on Adviser {\n        id\n        logo\n        name\n        job\n        surname\n        title\n        suffix\n        __typename\n      }\n      __typename\n    }\n    page\n    perPage\n    total\n    totalPages\n    __typename\n  }\n  badges\n  iovoxNumber\n  isDirectEnquiriesEnabled\n  isIovoxEnabled\n  isBranchUnavailable\n  isNew\n  latitude\n  linkedin\n  longitude\n  phone\n  preferredClientAssetsValue\n  preferredClientMortgageValue\n  preferredClientPensionValue\n  primaryAdviceAreas {\n    ...primaryAdviceArea\n    adviceAreas {\n      ...adviceArea\n      __typename\n    }\n    __typename\n  }\n  productType\n  profileSlug\n  responseRating\n  responseTime\n  restriction {\n    ...restriction\n    __typename\n  }\n  salesPitch\n  serviceSlug\n  showDefaultMortgageCompliance\n  skype\n  testimonials {\n    total\n    __typename\n  }\n  region\n  county\n  town\n  twitter\n  videoUrl\n  website\n  whatWeDo\n  layoutOptions {\n    ...layoutOptions\n    __typename\n  }\n  __typename\n}\n\nfragment awardWinnerBadge on AwardWinnerBadge {\n  type\n  badge\n  __typename\n}\n\nfragment primaryAdviceArea on PrimaryAdviceArea {\n  adviceAreas {\n    ...adviceArea\n    __typename\n  }\n  assetValues\n  id\n  name\n  __typename\n}\n\nfragment adviceArea on AdviceArea {\n  name\n  id\n  __typename\n}\n\nfragment restriction on Restrition {\n  name\n  code\n  __typename\n}\n\nfragment layoutOptions on LayoutOptions {\n  gtmLabel\n  showLogo\n  showFollowOptions\n  showDescription\n  showTestimonials\n  showSalesPitch\n  showAdviceAreas\n  showPreferredClientsAndPaymentOptions\n  showAccessibility\n  showPhoneNumber\n  clickToRevealPhoneNumber\n  advisers {\n    enableDialog\n    showName\n    showLogo\n    showAccreditations\n    showQualificationsAndAwards\n    __typename\n  }\n  __typename\n}\n',
    }

    Profile_response = requests.post('https://www.unbiased.co.uk/directory-api/graphql', headers=headers, json=json_data)

    # print(response.content)

    Advisers_html = Advisers_response.content
    Advisers_string_content = Advisers_html.decode('utf-8')

    Profile_html = Profile_response.content
    Profile_string_content = Profile_html.decode('utf-8')

    # Convert string to JSON
    Advisers_json_data = json.loads(Advisers_string_content)
    Profile_json_data = json.loads(Profile_string_content)

    advisers_info = Advisers_json_data['data']['profile']['advisers']['items']

    iovox_number = Profile_json_data['data']['profile']['iovoxNumber']
    address = Profile_json_data['data']['profile']['address']
    website = Profile_json_data['data']['profile']['website']
    linkedin = Profile_json_data['data']['profile']['linkedin']

    # Converting the advisers' information to JSON format
    formatted_output_json = []
    for adviser in advisers_info:
        adviser_info = {
            "title": adviser.get('title', ''),
            "name": adviser.get('name', ''),
            "surname": adviser.get('surname', ''),
            "job": adviser.get('job', ''),
            "qualifications": [q['qualification'] for q in adviser.get('qualifications', [])]
        }
        formatted_output_json.append(adviser_info)
    
    # Convert to JSON string
    json_formatted_string = json.dumps(formatted_output_json, indent=4)
    return json_formatted_string


if __name__ == "__main__":
    profiles = get_url_id('gu216nn')
    # get_managers_info(id)
    Profiles = json.loads(profiles)
        
        
    formatted_output_json = []
    for profile in Profiles:
        # Get manager's information based on ID as a string
        advisers_info_str = get_managers_info(profile['id'])

        # Parse the string as JSON
        try:
            advisers_info = json.loads(advisers_info_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for ID: {profile['id']}")
            continue

        # Function to process qualifications
        def process_qualifications(qualifications):
            if all(isinstance(q, dict) for q in qualifications):
                return [q['qualification'] for q in qualifications if 'qualification' in q]
            elif all(isinstance(q, str) for q in qualifications):
                return qualifications
            return []

        # Check and handle if advisers_info is a dictionary
        if isinstance(advisers_info, dict):
            # Process the dictionary
            adviser_details = {
                "title": advisers_info.get('title', ''),
                "name": advisers_info.get('name', ''),
                "surname": advisers_info.get('surname', ''),
                "job": advisers_info.get('job', ''),
                "qualifications": process_qualifications(advisers_info.get('qualifications', []))
            }

            combined_info = {
                "url": profile['url'],
                "id": profile['id'],
                **adviser_details
            }
            formatted_output_json.append(combined_info)

        # Handle if advisers_info is a list
        elif isinstance(advisers_info, list):
            # Process each item in the list
            for adviser in advisers_info:
                adviser_details = {
                    "title": adviser.get('title', ''),
                    "name": adviser.get('name', ''),
                    "surname": adviser.get('surname', ''),
                    "job": adviser.get('job', ''),
                    "qualifications": process_qualifications(adviser.get('qualifications', []))
                }

                combined_info = {
                    "url": profile['url'],
                    "id": profile['id'],
                    **adviser_details
                }
                formatted_output_json.append(combined_info)
        else:
            print(f"Unexpected data type after JSON parsing for ID {profile['id']}")

    # Convert to JSON string
    json_formatted_string = json.dumps(formatted_output_json, indent=4)
    with open('extracted_script2222.json', 'w', encoding='utf-8') as file:
        file.write(json_formatted_string)
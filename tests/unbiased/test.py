from bs4 import BeautifulSoup
import requests


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
    'https://www.unbiased.co.uk/advisers/financial-adviser?adviceArea=Investments&secondaryAdviceArea&search=gu21%206nn&searchId=22573650&assetValue=%C2%A3101,000%2B',
    headers=headers,
)

# print(response.content)
html_сontent = response.content

soup = BeautifulSoup(html_сontent, 'html.parser')

# Находим последний элемент <script>
last_script = soup.find_all('script')[-13]

# Выводим содержимое последнего элемента <script>
last_script_script = last_script.string

print(last_script_script)
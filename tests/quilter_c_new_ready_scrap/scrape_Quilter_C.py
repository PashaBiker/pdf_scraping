import json
from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests


def scrape_links(file_urls):

    pdf_links = {}

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')
        if key in pdf_links:
            print('PDF link of ' + key + ' already exists.')
            continue

        try:
            with requests.Session() as session:
                
                headers = {
                    'authority': 'www.quiltercheviot.com',
                    'accept': '*/*',
                    'accept-language': 'ru-RU,ru;q=0.9',
                    # 'cookie': 'TiPMix=28.286451342979035; x-ms-routing-name=self; ASP.NET_SessionId=v4rffjah2y0gsx4f2mkcu5th; LoginLink=#; LoginTitle=; LoginLinkTarget=_blank; ARRAffinity=cbd2540bbcc66a11a1cd3b4afaf05055f5511339815280fc150123d4f378cab4; ARRAffinitySameSite=cbd2540bbcc66a11a1cd3b4afaf05055f5511339815280fc150123d4f378cab4; DoNotForgetLoginAgain=5/10/2022%2010:10:00%20AM; ai_user=BeupU|2023-12-17T08:43:31.453Z; SeenCookieMessage=true; OptanonAlertBoxClosed=2023-12-17T08:43:33.160Z; SavedOTCookies=true; Region=uk; Role=fadv; fadv-LoginLink=#; fadv-LoginTitle=; fadv-LoginLinkTarget=_blank; _gcl_au=1.1.564106042.1702802613; _gid=GA1.2.809606775.1702802614; _pk_testcookie.04f5a3851ab5479d98c75aab2c09a376.d3d5=1; _pk_id.04f5a3851ab5479d98c75aab2c09a376.d3d5=9e45ee740f3e334a.1702802614.1.1702802614.1702802614.; _pk_ses.04f5a3851ab5479d98c75aab2c09a376.d3d5=1; _fbp=fb.1.1702802613788.871839820; _cs_c=1; _cs_id=5fde54c2-54fc-a64d-bc55-c22d36ebde65.1702802613.1.1702802613.1702802613.1.1736966613856; _ga=GA1.2.321584681.1702802614; _cs_s=1.5.0.1702804414170; ai_session=Tr4FB|1702802611554|1702802742842.5; _ga_YEP4E3ETBZ=GS1.1.1702802613.1.0.1702802777.60.0.0; _ga_RCC26TFV4G=GS1.1.1702802613.1.0.1702802777.0.0.0; _ga_SV2T56L986=GS1.1.1702802613.1.0.1702802777.0.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+17+2023+10%3A46%3A17+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=14ae850e-aa4a-49c4-ad63-10f63ccaf239&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=UA%3B68&AwaitingReconsent=false',
                    'referer': 'https://www.quiltercheviot.com/documents/?filters=170312%2c170309%2c170308%2c170310%2c116472&Region=uk&Role=fadv',
                    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                }

                params = {
                    'filters': '170312,170309,170308,170310,116472',
                    'superCategory': 'documents',
                    'pageSize': '12',
                    'role': 'fadv',
                    'region': 'uk',
                    'selectedFilters': '170312,170309,170308,170310,116472',
                    'lockedFilters': '',
                    'page': '1',
                }

                for page_num in [1, 2]:
                    params['page'] = str(page_num)
                    
                    response = requests.get('https://www.quiltercheviot.com/api/search/carmesitesearch/', params=params, headers=headers)

                    # Break the loop if the status code isn't 200 (OK)
                    if response.status_code != 200:
                        print(f"Error: Received status code {response.status_code}")
                        break

                    byte_string = response.content
                    decoded_string = byte_string.decode('utf-8')
                    data = json.loads(decoded_string)
                    print(data['page'])
                    # Break the loop if no more items

                    for item in data["items"]:
                        title = item["title"]
                        content_url = "https://www.quiltercheviot.com/" + item["contentUrl"]
                        pdf_links[title] = content_url
                    print(pdf_links)
                    # Increment the page number for the next iteration

        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        print(pdf_links)
    return pdf_links


def get_urls(spreadsheet):
    print('Getting URLs from spreadsheet...')
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets['PDF Scraping']

        pdf_url_range = sheet.range('B2').expand('down').value
        pdf_name_range = sheet.range('C2').expand('down').value

        file_urls = dict(zip(pdf_name_range, pdf_url_range))

        return file_urls

    except Exception as e:
        traceback.print_exc()

    finally:
        wb.save()
        wb.close()


def write_to_sheet(pdf_link, spreadsheet):

    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets['PDF Scraping']

        range_values = sheet.range('C1').expand('down').value

        for key, value in pdf_link.items():  
            for i, row in enumerate(range_values):
                if key == row:
                    print('Writing PDF link of ' + key + '...')
                    cell = sheet.range('D' + str(i + 1))
                    cell.value = value

    except Exception as e:
        traceback.print_exc()

    finally:
        wb.save()
        wb.close()




if __name__ == '__main__':
    # enter the name of the excel file
    # excel_file = 'tests/quilter cheviot/Quilter Cheviot Investment Manager.xlsm'
    excel_file = 'Quilter Cheviot Investment Manager.xlsm'
    # excel_file = 'tests/quilter_c_new/Quilter Cheviot Investment Manager.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

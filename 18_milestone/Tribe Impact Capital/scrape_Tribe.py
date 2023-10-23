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
                    'accept': '*/*',
                    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    # 'cookie': 'TiPMix=4.871320056368534; x-ms-routing-name=self; ASP.NET_SessionId=tbp251iveiqmsa2p1m4sf35c; LoginLink=#; LoginTitle=; LoginLinkTarget=_blank; ARRAffinity=48acf0709bf403e3643c99eaa23898057d24fe295bd6cb60b811b2a4ff6a671a; ARRAffinitySameSite=48acf0709bf403e3643c99eaa23898057d24fe295bd6cb60b811b2a4ff6a671a; ai_user=Zi2Sk|2023-10-20T16:28:55.670Z; SeenCookieMessage=true; OptanonAlertBoxClosed=2023-10-20T16:28:56.886Z; SavedOTCookies=true; Region=uk; Role=adv; _gid=GA1.2.2120528760.1697819337; _pk_testcookie.1ebac0a22195446c86fe38fd3c4c82e4.cbdf=1; _cs_c=1; __qca=P0-1513236584-1697819337249; _cs_cvars=%7B%221%22%3A%5B%22Role%22%2C%22Adviser%22%5D%7D; DoNotForgetLoginAgain=4/6/2023%203:20:00%20PM; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Oct+20+2023+20%3A08%3A56+GMT%2B0300+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; adv-LoginLink=#; adv-LoginTitle=; adv-LoginLinkTarget=_blank; ai_session=MsmYR|1697821736235.5|1697821736235.5; _cs_mk_ga=0.5346921596958463_1697821736273; _cs_mk=0.8506401839693998_1697821736280; _gat_UA-8115476-26=1; _gat_UA-8115476-24=1; _pk_id.1ebac0a22195446c86fe38fd3c4c82e4.cbdf=3bb02d171b9ea517.1697819337.2.1697821736.1697821736.; _pk_ses.1ebac0a22195446c86fe38fd3c4c82e4.cbdf=1; _ga=GA1.1.494975907.1697819337; _ga_ZZXRPHX6G1=GS1.1.1697821735.2.1.1697821736.0.0.0; _cs_id=88b2bcdc-2c7b-a4d9-a620-1f27898aacb1.1697819337.2.1697821736.1697821691.1.1731983337596; _cs_s=2.5.0.1697823536722',
                    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                }

                response = requests.get(url, headers=headers)
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')

                articles = soup.select('.flag__heading a')

                pdf_links = {article.get_text().strip(): article['href'] for article in articles}

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
    excel_file = '18_milestone\Tribe Impact Capital\Tribe Impact Capital.xlsm'
    # excel_file = 'Tribe Impact Capital.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

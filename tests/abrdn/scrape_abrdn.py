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
                    'authority': 'www.abrdn.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cache-control': 'max-age=0',
                    # 'cookie': 'abrdnjssintermediary#lang=en-GB; ASP.NET_SessionId=g5w1wkaixxe1m3xrfxrbjhma; _gcl_au=1.1.1667216191.1699705408; _cs_mk_ga=0.7863343682150521_1699705408257; _ga=GA1.2.1736705010.1699705408; _gid=GA1.2.1106109460.1699705408; _cs_c=1; ORA_FPC=id=e5c4bcc8-51cb-4f60-b8c9-6e2db608125e; ELOQUA=GUID=F08CFB3247EB40C5832601026BA2C1D5; OptanonAlertBoxClosed=2023-11-11T12:23:31.746Z; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Nov+11+2023+14%3A23%3A31+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=51313364-9372-4082-a713-65997245f8ce&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; abrdn-disclaimer=%5B%7B%22n%22%3A%22abrdnJssIntermediary%22%2C%22e%22%3A1707481412622%2C%22l%22%3A%22en-GB%22%7D%5D; WTPERSIST=; bluekai_uid_plugin=ora.odc_dmp_bk_uuid,OofHvV9u999V2iJA,ora.odc_dmp_bk_uuid_noslash,OofHvV9u999V2iJA,ora.odc_source,bluekai; _cs_id=97699ae7-54fc-a6cf-ad0b-e34d8c292c6e.1699705408.1.1699705431.1699705408.1.1733869408962; _cs_s=4.0.0.1699707231857; _gat_UA-65951746-1=1; _gat_UA-131211711-22=1; _ga_TML7E2DDE5=GS1.1.1699705408.1.1.1699705582.60.0.0',
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
                    'tab': '4',
                }

                response = session.get(
                    'https://www.abrdn.com/en-gb/intermediary/investment-solutions/managed-portfolio-service/literature',
                    params=params,
                    # cookies=cookies,
                    headers=headers,
                )

            # print(response.content)

            # Assuming 'response.content' contains your HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all relevant div tags
            divs = soup.find_all('div', class_='faded-underline col-12 py-3')

            pdf_links = {}  # Dictionary to store the links

            # Extract the necessary information from each div
            for div in divs:
                a_tag = div.find('a', class_='sitecore-link')
                if a_tag:
                    text = a_tag.get_text(strip=True).replace('\ufeff', '')
                    href = a_tag.get('href')
                    
                    # Check if the text is already in the pdf_links dictionary
                    if text not in pdf_links:
                        pdf_links[text] = href 
                   
        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)  
        print(pdf_links)
        # breakpoint()
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
    excel_file = 'abrdn.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

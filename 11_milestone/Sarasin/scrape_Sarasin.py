from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests
import re
from datetime import datetime

def scrape_links(file_urls):

    pdf_links = {}
    link_dict = {}

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')
        if key in pdf_links:
            print('PDF link of ' + key + ' already exists.')
            continue

        try:
            with requests.Session() as session:
                
                headers = {
                    'accept': '*/*',
                    'accept-language': 'ru-RU,ru;q=0.9',
                    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                }

                response = requests.get(url, headers=headers)
                request_content = response.content
                soup = BeautifulSoup(request_content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    if '.pdf' in link['href']:
                        # Ищем родительский контейнер для данной ссылки
                        parent_div = link.find_parent('div', class_="document-column")
                        
                        # Если такой контейнер найден, ищем текст внутри него
                        if parent_div:
                            title_text = link.get_text(strip=True)
                            pdf_links[title_text] = link['href']

                # Print the dictionary
                # for key, value in pdf_links.items():
                #     print(key, ':', value)

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
                if row == key:
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
    excel_file = 'Sarasin and Partners.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

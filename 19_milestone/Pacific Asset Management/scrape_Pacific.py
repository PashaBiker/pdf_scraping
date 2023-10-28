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
                    'authority': 'www.pacificam.co.uk',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cache-control': 'max-age=0',
                    # 'cookie': '_ga=GA1.1.503623669.1698181033; search_suggestions_session_id=65382fad38989; PHPSESSID=65382fad38989; investor_type=retail; _ga_5ZXCNWJFG9=GS1.1.1698425784.2.0.1698425784.60.0.0',
                    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                }

                response = requests.get(url, headers=headers)
                html = response.content
                # print(html)
                # breakpoint()
                soup = BeautifulSoup(html, 'html.parser')

                # Find all divs with the specified class
                divs = soup.find_all('ul', class_='elementor-icon-list-items')
                # print(divs)
                # Iterate over each div
                for div in divs:
                    # For each div, find all anchor tags
                    for a_tag in div.find_all('a'):
                        # Get the name (text inside the anchor tag) and the URL (href attribute)
                        name = a_tag.get_text(strip=True)
                        url = a_tag['href']
                        
                        if 'uploads' in url:
                            print(name, url)
                            # Store the name and URL in the result dictionary
                            pdf_links[name] = url

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
    excel_file = '19_milestone\Pacific Asset Management\Pacific Asset Management.xlsm'
    # excel_file = 'Pacific Asset Management.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

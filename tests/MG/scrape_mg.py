import requests
from bs4 import BeautifulSoup
import xlwings as xw
import traceback


def scrape_links(file_urls):
    pdf_links = {}

    for key, url in file_urls.items():
        print('Scraping link of ' + key + '...')
        if key in pdf_links:
            print('PDF link of ' + key + ' already exists.')
            continue
        with requests.Session() as session:
                
                headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                        }
                
                # Второй запрос (с теми же куками, заголовками сеанса и дополнительными headers)
                response = session.get(url, headers=headers)

                page_source = response.text
                # Ищем все элементы с тегом <a>, содержащие текст "Download Factsheets"
                soup = BeautifulSoup(page_source, 'html.parser')

                li_elements = soup.find_all('li', class_='listoflinks__list-item')

                for li in li_elements:
                    a_tag = li.find('a', class_='listoflinks__link')
                    if a_tag:
                        name = a_tag.find('span', class_='listoflinks__link-label-title').text.strip()
                        url = a_tag['href']
                        pdf_links[name] = url

    # for key, value in pdf_links.items():
    #     print(key + ': ' + value)

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
    excel_file = 'M&G Wealth Investments LLP.xlsm'
    excel_file = 'tests\MG\M&G Wealth Investments LLP.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

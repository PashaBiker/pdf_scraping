from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests
import re

all_pdf_links = {}

def add_content(all_content, driver):
    content = driver.page_source  
    return all_content + content

def html_url(url_part):
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'Accept': 'text/html, */*; q=0.01',
        'Referer': 'https://www.lgtwm.com/uk-en/financial-advisers/publications-for-financial-advisers/factsheets',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }

    page_num = 0

    while True:
        params = {
            'pageNum': str(page_num),
            'view': 'asList',
        }
        
        response = requests.get(f'https://www.lgtwm.com/service/pagination/uk-en/{url_part}', params=params, headers=headers)
        
        if '.pdf' not in response.text:
            break  # прерываем цикл, если в ответе нет .pdf
        
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_links = {}
        
        for div in soup.find_all('div', class_='lgt-teaser-list__element'):
            title_div = div.find('h3', class_='lgt-teaser__title')
            link = div.find('a', href=True)

            if title_div and link and '.pdf' in link['href']:
                title_text = title_div.get_text().strip()
                full_link = "https://www.lgtwm.com" + link['href']
                pdf_links[title_text] = full_link
        
        all_pdf_links.update(pdf_links)

        page_num += 1  # увеличиваем номер страницы на 1
    print(all_pdf_links)
    return all_pdf_links

def scrape_links(file_urls):
    pdf_links = {}

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')
        if key in pdf_links:
            print('PDF link of ' + key + ' already exists.')
            continue

        try:
            
            # print(file_urls)
            numbers = [match.group(1) for match in map(lambda x: re.search(r'_(\d+)$', x), file_urls.values()) if match]
            print(numbers)
            for num in numbers:
                pdf_links = (html_url(num))
            for key, value in pdf_links.items():
                print(key, ':', value)

        except Exception as e:
            print("An error occurred:", e)
    print(pdf_links)
    return pdf_links


def remove_duplicate_urls(file_urls):
    seen_urls = set()
    unique_urls = {}

    for key, url in file_urls.items():
        if url not in seen_urls:
            unique_urls[key] = url
            seen_urls.add(url)
    return unique_urls

def get_urls(spreadsheet):
    print('Getting URLs from spreadsheet...')
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets['PDF Scraping']

        pdf_url_range = sheet.range('B2').expand('down').value
        pdf_name_range = sheet.range('C2').expand('down').value

        file_urls = dict(zip(pdf_name_range, pdf_url_range))
        file_urls = remove_duplicate_urls(file_urls)
        # print(file_urls)

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
    excel_file = 'LGT Wealth Management.xlsm'
    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)
    print('Done!')

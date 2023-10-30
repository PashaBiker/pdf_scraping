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
        if key in link_dict:
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
                pdf_links = []
                # Find the div with the class 'facetwp-template'
                facetwp_div = soup.find('div', class_='facetwp-template')
                for a_tag in facetwp_div.find_all('a', class_='port-item'):
                    # print(a_tag)
                    title_tag = a_tag.find('span', class_='port-title').text
                    title = title_tag.strip()  # e.g., 'OBI Active 5'
                    # print(title_tag)
                    content_url = a_tag['href']
                    # print(content_url)
                    pdf_links.append(f"{title}:{content_url}")
                # print(pdf_links)
                
                def extract_date_from_url(url):
                    # Извлекаем дату из URL
                    match = re.search(r"(\d{4}/\d{2})", url)
                    if match:
                        date_str = match.group(1)
                        return datetime.strptime(date_str, "%Y/%m")
                    return None

                # Извлекаем даты из каждой ссылки
                dates_and_links = [(extract_date_from_url(link), link) for link in pdf_links]

                # Убираем None значения
                dates_and_links = [dl for dl in dates_and_links if dl[0] is not None]

                # Находим самую свежую дату
                latest_date = max(dates_and_links, key=lambda x: x[0])[0]

                # Возвращаем все ссылки с самой свежей датой
                latest_links = [link for date, link in dates_and_links if date == latest_date]

                # print(latest_links)
                for item in latest_links:
                    key, value = item.split(":", 1)  # разделяем по первому вхождению ':'
                    link_dict[key] = value

                # Print the dictionary
                # for key, value in pdf_links.items():
                #     print(key, ':', value)

        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        print(link_dict)
    return link_dict


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
    # excel_file = 'OCM Asset Management.xlsm'
    excel_file = '9_milestone\OCM Asset Management.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

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
                    'referer': 'https://www.quiltercheviot.com/literature/?query=&sortBy=null&supercategory=literature&category=521',
                    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                }

                response = session.get(url, headers=headers)

                page_source = response.text
                soup = BeautifulSoup(page_source, 'html.parser')
                # pdf_links_all = soup.find_all('a', href=True)
                # for link in pdf_links_all:       
                #     pdf_links[link.text] = link['href']
                base_url = 'https://maia-am.co.uk/'
                for link in soup.find_all('a', href=True):
                    if '.pdf' in link['href']:
                        # Достаём название PDF из блока с классом "module__downloads__item__name"
                        name_div = link.find('div', class_='module__downloads__item__name')
                        if name_div:
                            pdf_name = name_div.text.strip()  # Удаляем лишние пробелы
                            
                            # Удаляем два последних слова
                            words = pdf_name.split()
                            if len(words) > 2:
                                pdf_name = ' '.join(words[:-2])

                            if 'maia-am.co.uk' in link['href']:
                                pdf_links[pdf_name] = link['href']
                            else:
                                pdf_links[pdf_name] = base_url + link['href']

                # Print the dictionary
                for key, value in pdf_links.items():
                    print(key, ':', value)

        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        # print(pdf_links)
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
    excel_file = 'MAIA Asset Management.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

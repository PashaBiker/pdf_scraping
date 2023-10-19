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
                    'accept-language': 'ru-RU,ru;q=0.9',
                    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                }

                response = session.get(url, headers=headers)
                request_content = response.content
                # print(request_content)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all anchor tags
                anchor_tags = soup.find_all('a')
                url = "https://www.arbuthnotlatham.co.uk/"
                # Create a dictionary
                links_dict = {}
                for tag in anchor_tags:
                    # Check if 'href' attribute exists and if it points to a PDF
                    if tag.has_attr('href') and tag['href'].endswith('.pdf'):
                        links_dict[tag.text.upper()] = url + tag['href']




        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        print(links_dict)
    return links_dict


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
    # excel_file = '17_milestone\Arbuthnot Latham\Arbuthnot Latham.xlsm'
    excel_file = 'Arbuthnot Latham.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

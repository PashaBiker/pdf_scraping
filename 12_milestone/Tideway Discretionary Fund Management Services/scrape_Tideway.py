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

                response = session.get(url, headers=headers)
                request_content = response.content
                soup = BeautifulSoup(request_content, 'html.parser')
                # print(soup)
                # breakpoint()
                # Find all the div elements with the class 'e-con-full e-flex e-con e-child'
                div_elements = soup.select('div.e-con-full.e-flex.e-con.e-child')

                for div in div_elements:
                    # Search for the h2 tag within each div to get the title
                    h2_tag = div.find('h2', class_='elementor-heading-title elementor-size-default')
                    if h2_tag:
                        title = h2_tag.text.strip()
                        # Search for the anchor tag with the relevant class to get the PDF link
                        a_tag = div.find('a', class_='elementor-button elementor-button-link elementor-size-sm')
                        if a_tag:
                            content_url = a_tag['href']
                            pdf_links[title] = content_url

                print(pdf_links)

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
    # excel_file = '12_milestone\Tideway Discretionary Fund Management Services\Tideway Discretionary Fund Management Services.xlsm'
    excel_file = 'Tideway Discretionary Fund Management Services.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

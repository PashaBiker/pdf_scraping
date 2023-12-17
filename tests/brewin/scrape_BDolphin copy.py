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
            headers = {
                'authority': 'www.brewin.co.uk',
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

            response = requests.get(url, headers=headers)


            
            page_source = response.text
            soup = BeautifulSoup(page_source, "html.parser")
            
            pdf_links = []
            print(soup.html)
            breakpoint()
            mps = soup.find('div', attrs={'data-id': 'managed-portfolio-service-factsheets-content'})
            ppm = soup.find('div', attrs={'data-id': 'passive-plus-mps-factsheets-content'})

            links_mps = mps.find_all('a') 
            name_mps = mps.find_all('h2') 
            links_ppm = ppm.find_all('a') 
            name_ppm = ppm.find_all('h2')
            url2 = 'https://www.brewin.co.uk/'

            # Добавляем атрибут href каждой ссылки в список pdf_links
            for i in range(len(links_mps)):
                name = name_mps[i].text.split(' – ')[0].split('\xa0')[0].strip()
                full_link = url2 + links_mps[i]['href']
                if full_link not in pdf_links:
                    pdf_links.append({name: full_link})

            for i in range(len(links_ppm)):
                name = name_ppm[i].text.split(' – ')[0].split('\xa0')[0].strip()
                full_link = url2 + links_ppm[i]['href']
                if full_link not in pdf_links:
                    pdf_links.append({name: full_link})





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

        for link in pdf_link:
            for key, value in link.items():
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
    excel_file = 'Brewin Dolphin.xlsm'
    excel_file = 'tests/brewin/Brewin Dolphin.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

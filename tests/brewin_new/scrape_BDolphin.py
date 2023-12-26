from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests


def scrape_links(file_urls):

    pdf_links =[]

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')

        # Check if key exists in any of the dictionaries inside pdf_links
        if any(key in d for d in pdf_links):
            print('PDF link of ' + key + ' already exists.')
            continue

        try:
            headers = {
                'authority': 'www.brewin.co.uk',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                # 'cookie': 'vip-go-seg=vc-v1__10_channel_--_intermediaries; _hjFirstSeen=1; _hjIncludedInSessionSample_942828=1; _hjSessionUser_942828=eyJpZCI6IjBkNWUwNjkzLWJjMjktNWMwNi05MDM2LTJjY2MwOWFhZTIwZCIsImNyZWF0ZWQiOjE3MDI3NjU3MzgwNjQsImV4aXN0aW5nIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _hjSession_942828=eyJpZCI6IjkzZWE2ZmI3LTY0YjQtNDRiNy04MTk4LTY4NzExMGY0MjczZCIsImMiOjE3MDI3NjU3MzgwNjUsInMiOjEsInIiOjEsInNiIjowfQ==; OptanonAlertBoxClosed=2023-12-16T22:29:05.615Z; _gcl_au=1.1.671755954.1702765746; _ga=GA1.1.716875567.1702765746; mid-disclaimer-10=accepted; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+17+2023+00%3A29%3A07+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=284e1a17-4f44-4fab-ab3c-f62ae63c05a6&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; _ga_2N7PQEQ4QC=GS1.1.1702765745.1.1.1702765747.0.0.0; _ga_BPH6CJ8P9F=GS1.1.1702765745.1.1.1702765747.0.0.0; _ga_CKMDK1SJ9M=GS1.1.1702765745.1.1.1702766418.0.0.0',
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

            response = requests.get(url, headers=headers)

            page_source = response.text
            soup = BeautifulSoup(page_source, "html.parser")
            
            base_url = "https://www.brewin.co.uk"  # Replace with the base URL of your website

            factsheets = {a.text: a['href'] for a in soup.find_all('a', class_='link-cta link-download')}

            # pdf_links = []  # Initialize pdf_links as a list

            for name, full_link in factsheets.items():
                # Check if the link is a relative URL
                if not full_link.startswith("http://") and not full_link.startswith("https://"):
                    full_link = base_url + full_link  # Prepend the base URL to make it absolute

                pdf_links.append({name: full_link})

        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        # print(pdf_links)
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
    # excel_file = 'tests/brewin/Brewin Dolphin.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

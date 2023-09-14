from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests


def scrape_links(file_urls):

    documents = {}

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')
        if key in documents:
            print('PDF link of ' + key + ' already exists.')
            continue

        try:
            headers = {
                'authority': 'www.brooksmacdonald.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

            response = requests.get(
                'https://www.brooksmacdonald.com/investment-management/factsheets-and-literature',
                headers=headers,
            )

            html_content = response.content

            soup = BeautifulSoup(html_content, 'html.parser')

            # Находим все div с нужным классом
            divs = soup.find_all('div', class_='document-item-wrapper')

            # Проходим по каждому div и извлекаем нужную информацию
            for div in divs[1:]:
                title_element = div.find('p', class_='doc-title').get_text(strip=True)
                link_element = div.find('a', class_='doc-link media-link')
                link = link_element['href']
                # Check if the elements exist before accessing them
                if title_element and link:

                    title = title_element
                    cleaned_title = title.split(" | ")[0]

                    # If href doesn't start with http or https, then prepend the base URL
                    if not link.startswith(('http', 'https')):
                        link = "https://www.brooksmacdonald.com" + link

                    # Check if this title already exists in documents
                    if cleaned_title in documents:
                        # If this link has 'Adviser' or 'adviser' and the existing one does not, replace the existing link
                        if ('Adviser' in link or 'adviser' in link) and not ('Adviser' in documents[cleaned_title] or 'adviser' in documents[cleaned_title]):
                            documents[cleaned_title] = link
                    else:
                        documents[cleaned_title] = link

        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        print(documents)
        # breakpoint()
    return documents


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

        for key, value in pdf_link.items():  # directly loop through pdf_link items
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
    excel_file = 'Brooks Macdonald.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

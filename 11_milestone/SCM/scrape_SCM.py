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
                'authority': 'scmdirect.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                # 'cookie': 'wpdiscuz_nonce_eec729cc2a7c804ab58f4de410a33d28=f020c8dfa3; _ga_S3NZQSRP7D=GS1.1.1692863309.1.0.1692863309.60.0.0; _ga=GA1.1.345230527.1692863309; _hjSessionUser_1358120=eyJpZCI6ImI5MDY5ZWNkLTgxYTItNTI0Ni04MTE0LTUzMDg5NDIyNWE1NCIsImNyZWF0ZWQiOjE2OTI4NjMzMDk0OTYsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample_1358120=1; _hjSession_1358120=eyJpZCI6ImU2MzdjMjVhLWUwMGYtNGZhNy05OGYzLWViODBkYmU2ODE4NCIsImNyZWF0ZWQiOjE2OTI4NjMzMDk1MjQsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; __hstc=216836425.3d1469c3f7c9e855eed6a94a115ac87f.1692863310180.1692863310180.1692863310180.1; hubspotutk=3d1469c3f7c9e855eed6a94a115ac87f; __hssrc=1; __hssc=216836425.1.1692863310181; ln_or=eyIxNjQ3MjczIjoiZCJ9',
                'referer': 'https://scmdirect.com/investment-portfolios/',
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                }

                response = session.get(url, headers=headers)
                request_content = response.content
                soup = BeautifulSoup(request_content, 'html.parser')

                pdf_links = {}  # To store the titles and their PDF links

                # Find the div with the class 'portfolios__list__item'
                portfolio_divs = soup.findAll('div', class_='portfolios__list__item')

                for portfolio_div in portfolio_divs:
                    # Find the 'h4' tag for the title
                    title_tag = portfolio_div.find('h4')
                    if title_tag:
                        title = title_tag.text.strip()  # e.g., 'SCM Bond Reserve'

                        # Find the 'a' tag with class 'btn btn--yellow' for the PDF link
                        pdf_a_tag = portfolio_div.find('a', class_='btn btn--yellow')
                        if pdf_a_tag:
                            pdf_url = pdf_a_tag['href']
                            pdf_links[title] = pdf_url

                print(pdf_links)

                # pdf_links = {}
                # pdf_links[title] = content_url

                # Print the dictionary
                # for key, value in pdf_links.items():
                #     print(key, ':', value)

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
    excel_file = 'SCM Private.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

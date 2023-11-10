import json
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
                
                
                cookies = {
                'RSMR_CONSENT_siteDisclaimer': 'isUKFinancialProfessional+20231108-17-29',
            }

            headers = {
                'authority': 'www.rsmr.co.uk',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'ru-RU,ru;q=0.9',
                # 'cookie': 'MXP_TRACKINGID=B6C40AE8-C6CA-4CEB-BF57A15C31AB9904; mobileFormat=false; cfid=85c46d17-0a41-4aab-8c62-ac0fa0917c28; cftoken=0; CF_CLIENT_MURA1159D3CF4C8818EDC92155CA70EE9F5C=%7B%22SESSIONCHECKED%22%3Atrue%7D; CF_CLIENT_MURA1159D3CF4C8818EDC92155CA70EE9F5C_TC=1699464406091; _pk_id.1.3c57=401a285263e9325c.1699464407.; _pk_ses.1.3c57=1; _gid=GA1.3.1652108519.1699464407; _ga=GA1.1.1302132073.1699464407; _ga_836ZEEZHXN=GS1.1.1699464406.1.1.1699464409.0.0.0; AWSALB=FMLqP8mCdPCZVx1zJkpWtOdro5xw+K9qnSmJ8hkbF4ORqVPg7ltkxi8zgFEt7COO6rmx3O7ziDfUnzob4SVKAtcaxLIDH2yZmukiccwKts/Y3qfT8LMI++F/bzKL; AWSALBCORS=FMLqP8mCdPCZVx1zJkpWtOdro5xw+K9qnSmJ8hkbF4ORqVPg7ltkxi8zgFEt7COO6rmx3O7ziDfUnzob4SVKAtcaxLIDH2yZmukiccwKts/Y3qfT8LMI++F/bzKL; RSMR_CONSENT_siteDisclaimer=isUKFinancialProfessional+20231108-17-29; CF_CLIENT_MURA1159D3CF4C8818EDC92155CA70EE9F5C_LV=1699464582704; CF_CLIENT_MURA1159D3CF4C8818EDC92155CA70EE9F5C_HC=12',
                'referer': 'https://www.rsmr.co.uk/?disclaimer&returnURL=https%3A%2F%2Fwww.rsmr.co.uk%2Fmanaged-portfolio-service%2Fyour-support%2F%3Fcdlresp%3D1',
                'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            }

            params = {
                'cdlresp': '1',
            }

            response = session.get(
                'https://www.rsmr.co.uk/managed-portfolio-service/your-support/',
                params=params,
                cookies=cookies,
                headers=headers,
            )

            # print(response.content)

            html_data = response.content

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html_data, 'html.parser')

            # Initialize an empty dictionary to store the results

            # Find the table by class name (if there are multiple tables you would need to refine this)
            tables = soup.findAll('table', class_='table table-hover documents-index no-hover')
            # print(tables)
            # Check if the table is found
            for table in tables:
                # Find all 'a' tags within the table
                rows = table.find_all('tr')
                for row in rows:
                    # Find the 'td' tag with class 'title' for the name
                    title_cell = row.find('td', class_='title')
                    if title_cell:
                        # Get the text and strip any whitespace characters
                        name = title_cell.get_text(strip=True)
                        # Find the 'a' tag for the URL
                        link = row.find('a', href=True)
                        if link and link['href'].startswith('http'):
                            # Get the href attribute
                            url = link['href']
                            # Add the name and URL to the dictionary
                            pdf_links[name] = url

                    
        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)  
        print(pdf_links)
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
    excel_file = 'Rayner Spencer Mills Research Limited.xlsm'
    excel_file = '19_milestone\Rayner Spencer Mills Research Limited\Rayner Spencer Mills Research Limited.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

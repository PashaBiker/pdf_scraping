from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def scrape_links(file_urls):

    pdf_links = {}
    fund_data = {}

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')
        if key in pdf_links:
            print('PDF link of ' + key + ' already exists.')
            continue
        try:
            
            driver = webdriver.Chrome()

            if '/fund/' in url:
                driver.get(url)
                # time.sleep(5)
                WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/div[12]/div/fx-document-group-panel/div/fx-documents-panel/div[2]/div/div[2]/div[2]/fx-document-item/div/a")))
                
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')


                



                
                driver.quit()

                div_tag = soup.find('div', {'class': 'fund-info valign-middle'})
                # Из этого div извлекаем текст из тега <strong> внутри <h1>
                fund_name_div = div_tag.h1.strong.text

                # Убираем " F Acc", если оно есть в тексте
                fund_name_text = fund_name_div.replace(' F Acc', '')
                anchor = soup.findAll('a', {'data-test-id': 'fundDashboardPageDocumentItem'})
                # for fund_name in anchor:
                #     # fund_name_text = fund_name.h2.text
                #     fact_sheet_link = fund_name['href']
                #     fund_data[fund_name_text] = fact_sheet_link
                for link in anchor:
                    title = link.find('h2')
                    if title and title.text.strip() == 'Factsheet':
                        fact_sheet_link = link['href']
                        fund_data[fund_name_text] = fact_sheet_link
                        print(fact_sheet_link)
            else:
                driver.get(url)
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".RelatedCardstyled__LinkWrapper-sc-1wbco6m-5")))
                page_source = driver.page_source

                driver.quit()
                
                soup = BeautifulSoup(page_source, 'html.parser')
                divs = soup.findAll('div', {'class': 'RelatedCardstyled__LinkWrapper-sc-1wbco6m-5'})
                for anchor in divs:
                    a_part = anchor.find('a', class_='TextLinkstyled__TextLinkStyled-sc-1yqvx22-0')
                    fund_name = a_part.div.text
                    fact_sheet_link = a_part['href']
                    fund_data[fund_name] = fact_sheet_link
                    print(fact_sheet_link)

        except requests.exceptions.RequestException as e:
            print("Error fetching the URL:", e)
        except Exception as e:
            print("An error occurred:", e)
        print(fund_data)
    return fund_data


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

        # If there's only one value, convert it to a list.
        if not isinstance(range_values, list):
            range_values = [range_values]

        for key, value in pdf_link.items():
            for i, row in enumerate(range_values):
                if row == key:
                    print('Writing PDF link of ' + key + '...')
                    cell = sheet.range('D' + str(i + 1))  # Adjusted the index to match the Excel row index.
                    cell.value = value
                    print('Link written for ' + key)
                    
    except Exception as e:
        traceback.print_exc()
    finally:
        wb.save()
        wb.close()





if __name__ == '__main__':
    # enter the name of the excel file
    # excel_file = 'Schroder Investment Solutions.xlsm'
    excel_file = '11_milestone\Schroder\Schroder Investment Solutions.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

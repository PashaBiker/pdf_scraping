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
from threading import Thread, Lock

fund_data_lock = Lock()
fund_data = {}

def scrape_one_link(key, url):
    print('Scraping PDF link of ' + key + '...')
    
    try:
        s = Service('chromedriver\chromedriver.exe')
        driver = webdriver.Chrome(service=s)

        if '/fund/' in url:
            driver.get(url)
            time.sleep(15)
            WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.XPATH, "//a[@data-test-id='fundDashboardPageDocumentItem']")))
            # time.sleep(5)
            page_source = driver.page_source
            print('fund')
            soup = BeautifulSoup(page_source, 'html.parser')
            div_tag = soup.find('div', {'class': 'fund-info valign-middle'})

            fund_name_div = div_tag.h1.strong.text
            fund_name_text = fund_name_div.replace(' F Acc', '')
            anchor = soup.findAll('a', {'data-test-id': 'fundDashboardPageDocumentItem'})
            with fund_data_lock:
                for fund_name in anchor:
                    fact_sheet_link = fund_name['href']
                    fund_data[fund_name_text] = fact_sheet_link
        else:
            driver.get(url)
            time.sleep(15)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".RelatedCardstyled__LinkWrapper-sc-1wbco6m-5")))
            page_source = driver.page_source
            print('fund2')

            soup = BeautifulSoup(page_source, 'html.parser')
            divs = soup.findAll('div', {'class': 'RelatedCardstyled__LinkWrapper-sc-1wbco6m-5'})
            with fund_data_lock:
                for anchor in divs:
                    a_part = anchor.find('a', class_='TextLinkstyled__TextLinkStyled-sc-1yqvx22-0')
                    fund_name = a_part.div.text
                    fact_sheet_link = a_part['href']
                    fund_data[fund_name] = fact_sheet_link

        driver.quit()

    except requests.exceptions.RequestException as e:
        print("Error fetching the URL:", e)
    except Exception as e:
        print("An error occurred:", e)

    print(fund_data)


def scrape_links(file_urls):
    threads = []

    for key, url in file_urls.items():
        thread = Thread(target=scrape_one_link, args=(key, url))
        threads.append(thread)
        thread.start()

    # Дождитесь завершения всех потоков:
    for thread in threads:
        thread.join()

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
    excel_file = 'Schroder Investment Solutions.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

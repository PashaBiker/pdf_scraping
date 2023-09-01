from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

def scrape_link(key, url):
    fund_data = {}

    try:
        s = Service('chromedriver\chromedriver.exe')
        driver = webdriver.Chrome(service=s)

        if '/fund/' in url:
            driver.get(url)
            time.sleep(5)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[@data-test-id='fundDashboardPageDocumentItem']")))
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')
            div_tag = soup.find('div', {'class': 'fund-info valign-middle'})

            fund_name_div = div_tag.h1.strong.text
            fund_name_text = fund_name_div.replace(' F Acc', '')
            anchor = soup.findAll('a', {'data-test-id': 'fundDashboardPageDocumentItem'})

            for fund_name in anchor:
                fact_sheet_link = fund_name['href']
                fund_data[fund_name_text] = fact_sheet_link

        else:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".RelatedCardstyled__LinkWrapper-sc-1wbco6m-5")))
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')
            divs = soup.findAll('div', {'class': 'RelatedCardstyled__LinkWrapper-sc-1wbco6m-5'})

            for anchor in divs:
                a_part = anchor.find('a', class_='TextLinkstyled__TextLinkStyled-sc-1yqvx22-0')
                fund_name = a_part.div.text
                fact_sheet_link = a_part['href']
                fund_data[fund_name] = fact_sheet_link

        driver.quit()

    except Exception as e:
        print(f"Error scraping {key}: {e}")

    return fund_data

def get_urls(spreadsheet):
    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets['PDF Scraping']

    pdf_url_range = sheet.range('B2').expand('down').value
    pdf_name_range = sheet.range('C2').expand('down').value

    file_urls = dict(zip(pdf_name_range, pdf_url_range))
    wb.close()
    return file_urls

def write_to_sheet(pdf_link, spreadsheet):
    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets['PDF Scraping']

    for key, value in pdf_link.items():
        cell = sheet.range(f"C:{len(pdf_link)+1}").find(key)
        if cell:
            row = cell.row
            sheet.range(f'D{row}').value = value

    wb.save()
    wb.close()

def main():
    excel_file = 'Schroder Investment Solutions.xlsm'
    file_urls = get_urls(excel_file)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_link, key, url) for key, url in file_urls.items()]

        for future in futures:
            pdf_link = future.result()
            write_to_sheet(pdf_link, excel_file)
            
    print('Done!')

if __name__ == '__main__':
    main()

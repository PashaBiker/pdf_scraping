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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_links(file_urls):

    pdf_links = {}

    for key, url in file_urls.items():
        print('Scraping PDF link of ' + key + '...')
        if key in pdf_links:
            print('PDF link of ' + key + ' already exists.')
            continue

        try:
            
            driver = webdriver.Chrome()

            driver.get(url)

            wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд
            time.sleep(5)
            # Ждем появления кнопки "Accept All" и кликаем по ней
            accept_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"cookiescript_accept\"]")))
            accept_all_button.click()
            wait.until(EC.invisibility_of_element_located((By.ID, "cookiescript_injected")))

            time.sleep(5)
            # driver.get(url)
            # Ждем появления элемента 'Financial Intermediary' и кликаем по нему
            fi_label = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[5]/div[2]/section[3]/div/div[1]/ul/li[3]')))
            fi_label.click()

            # Ждем появления элемента 'I Accept' и кликаем по нему
            i_accept_label = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[5]/div[2]/form/section/div/div/div[2]/div/label[1]")))
            i_accept_label.click()

            # Ждем появления кнопки "Proceed" и кликаем по ней
            proceed_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.dialogs > div.popup.selfCertProfile-popup > div.disclaimer.col > form > section > div > div > div.disclaimer-actions.align-items-start > a')))
            proceed_button.click()
            time.sleep(5)

            # Копируем исходный код страницы
            page_source = driver.page_source

            driver.quit()


            soup = BeautifulSoup(page_source, 'html.parser')

            fund_elements = soup.find_all('tr')

            for fund_element in fund_elements:
                fund_name_element = fund_element.find(attrs={"data-bind": "text: FundName"})
                if fund_name_element:
                    fund_name = fund_name_element.text.strip().upper()

                    fact_sheet_link_element = fund_element.find('a', text='EN')
                    if fact_sheet_link_element:
                        fact_sheet_link = fact_sheet_link_element['href']
                        pdf_links[fund_name] = fact_sheet_link

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
    excel_file = 'GAM.xlsm'
    # excel_file = '10_milestone\GAM.xlsm'

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print('Done!')

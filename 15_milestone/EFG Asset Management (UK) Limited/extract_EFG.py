import os
import traceback
import PyPDF2
import requests
import xlwings as xw
from PyPDF2 import PdfReader
import re
import glob
import time
import PyPDF2
import pdfplumber
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

excel_file = 'EFG Asset Management (UK) Limited.xlsm'

def get_data(url):
        
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait until the specific element appears and click the button
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="investorType"]/div/div/div/a[1]'))
    element = WebDriverWait(driver, 30).until(element_present)

    button = driver.find_element(By.XPATH, '//*[@id="investorType"]/div/div/div/a[1]')
    button.click()

    element_accept = EC.presence_of_element_located((By.XPATH,'//*[@id="modalDisclaimer"]/div/div/div/div/div[1]/div[1]/div[2]/div/a[1]'))
    element = WebDriverWait(driver, 30).until(element_accept)


    button = driver.find_element(By.XPATH,'//*[@id="modalDisclaimer"]/div/div/div/div/div[1]/div[1]/div[2]/div/a[1]')
    time.sleep(2)  # Дайте немного времени после скролла перед тем, как кликнуть
    button.click()
    time.sleep(2)  # Дайте немного времени после скролла перед тем, как кликнуть

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    # Нахождение всех div с определенным классом
    isin_parts = url.split("isin=")
    isin = isin_parts[1]
    divs_bg_pastel = soup.findAll('div', class_='table-performance',id=isin)
    additional_information = ''
    # Performance details
    for table_info in divs_bg_pastel:
        additional_information += str(table_info.find('div', class_='bg-pastel-type-multi_asset pt-2'))
        # print(additional_information)
        
    # Performance details

    # Breakdown

    divs_ajax_component = soup.find_all('div', class_='ajax-component component-lg')

    result = []
    driver.quit()

    soup = BeautifulSoup(additional_information, 'html.parser')

    # Извлечение даты
    date = soup.find('th', width="55%").text.strip().split()[-1].replace('-',' ')
    print(f"Date: {date}")

    # Извлечение значения для 1 месяца
    one_month = soup.find('th', text='1 Month').find_next('td').text.strip('%')
    print(f"1 Month: {one_month}%")

    # Извлечение значения для 1 года
    one_year = soup.find('th', text='1Yr').find_next('td').text.strip('%')
    print(f"1 Year: {one_year}%")

    # Извлечение значения OCF
    OCF = soup.find(string='Ongoing Charges Figure (OCF):').find_next().text.strip('%')
    print(f"OCF: {OCF}%")

    for tables_all in divs_ajax_component:
        tables = tables_all.find_all('table', class_='table table-chart component')
        
        # Если таблица не пустая
        if tables:
            for table in tables:
                data = {}  # словарь для хранения пар ключ-значение из каждой таблицы
                rows = table.find_all('tr')
                
                for row in rows:
                    key = row.find('th').text.strip()
                    value = float(row.find('td').text.strip().replace('%', ''))
                    if key in data:
                        data[key] += value  # Если ключ уже существует, прибавляем к его текущему значению новое значение
                    else:
                        data[key] = value
                    
                    # total += float(value)
                result.append(data)

    asset_values = {}
    for d in result:
        asset_values.update(d)

    # Вычисляем сумму всех чисел
    total_sum = sum(asset_values.values())
    print(asset_values)
    print(total_sum)

    return one_year,one_month, asset_values, OCF, date

def write_to_sheet(one_year,one_month, assets, OCF, spreadsheet, filename, date):

    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)

        sheet = wb.sheets[2]

        # search the model keys in the first column
        range_values = sheet.range('A1').expand().value

        for i, row in enumerate(range_values):
            if filename in row:
                print('Writing Portfolio cost for', filename)

                cellb = sheet.range('B'+str(i+1))
                cellb.value = date

                cellc = sheet.range('C'+str(i+1))
                cellc.value = float(OCF)/100
                cellc.number_format = '0.00%'

                celld = sheet.range('D'+str(i+1))
                celld.value = float(one_year)/100
                celld.number_format = '0.00%'

                celle = sheet.range('E'+str(i+1))
                celle.value = float(one_month)/100
                celle.number_format = '0.00%'

        wb.save()

        sheet = wb.sheets[3]

        column_headings = sheet.range('A1').expand('right').value

        for asset in assets:
            if asset not in column_headings:
                # Find the first empty column dynamically
                empty_column_index = len(column_headings) + 1
                empty_column = column_letter_from_index(empty_column_index)

                # Assign the asset value to the first empty column
                cell = sheet.range(f'{empty_column}1')
                cell.value = asset

                # Append the asset to column_headings
                column_headings.append(asset)

        # search the model keys in the first column
        range_values = sheet.range('A1').expand().value

        for i in range(len(range_values)):
            if filename in range_values[i]:
                print('Writing asset values for', filename)
                for asset, value in assets.items():
                    column_index = column_headings.index(asset) + 1
                    cell = sheet.range(
                        f'{column_letter_from_index(column_index)}{i+1}')
                    cell.value = float(str(value).replace(',', '')) / 100
                    cell.number_format = '0.00%'


    except Exception as e:
        print(f"An error occurred in file {filename}: {str(e)}")
        traceback.print_exc()

    finally:
        wb.save()
        wb.close()
        app.quit()

def filenames(spreadsheet):
    
    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets[1]
    filenames_list = []
    urls_list = []
    # Start from row 3 and iterate through the links in column B
    last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row
    for row in range(3, last_row+1):
        # Get the corresponding filename from column A
        filename = sheet.range(f'A{row}').value
        filenames_list.append(filename)
        url = sheet.range(f"B{row}").value
        urls_list.append(url)
        # Download the PDF from the link
    
    wb.close()
    app.quit()
    
    return filenames_list, urls_list

def column_letter_from_index(index):
    result = ""
    while index > 0:
        index -= 1
        remainder = index % 26
        result = chr(65 + remainder) + result
        index = index // 26
    return result


if __name__ == '__main__':

    
    filenames, urls = filenames(excel_file)
    for filename, url in zip(filenames, urls):
        one_year, one_month, assets, OCF, date = get_data(url)
        write_to_sheet(one_year, one_month, assets, OCF, excel_file, filename, date)

    print('\nDone!')

import os
import traceback
import PyPDF2
import requests_html
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

excel_file = '16_milestone\BlackRock\BlackRock.xlsm'

def get_data(url):
    AMC = 0.0
    driver = webdriver.Chrome()
    driver.get(url)

    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="performance"]'))
    WebDriverWait(driver, 30).until(element_present)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(date_text)

    cumulative_div = soup.find("div", {"id": "subTabCumulative"})

    date = cumulative_div.find('option', selected=True).get_text(strip=True).replace('/', ' ')
    one_month = cumulative_div.find('td', class_='oneMonth').get_text(strip=True)
    one_year = cumulative_div.find('td', class_='oneYear').get_text(strip=True)

    # print(ocf_text)
    # OCF = re.search(r'(\d+\.\d+)', ocf_text).group(1)
    # print(ocf)
    # print(one_month_one_year_text[2])

    OCF = soup.find('div', class_='col-onch').find('span', class_='data').text.replace('%','')
    try:
        AMC = soup.find('div', class_='col-mer').find('span', class_='data').text
    except:
        AMC = 0.0

    # print(f'Ongoing Charges Figures: {ongoing_charges_figures}')
    # print(f'Annual Management Fee: {annual_management_fee}')
            
    print(date)
    print(one_month)
    print(one_year)
    print(OCF)
    print(AMC)
    # print(assets_text)
    # Find all 'tr' elements within the 'tbody' tag

    # Extract all rows (tr elements) from the table
    # Parse the HTML content using Beautiful Soup
    # Iterate through each row in the table's body

    # Разбор содержимого HTML с помощью Beautiful Soup

    # Извлечение всех div-элементов с классом "fund-component column"
    divs = soup.find_all("div", {"class": "table-chart-container col-2 column grid"})


    data = []

    for div in divs:
        # Извлечение всех элементов tr для каждого div
        rows = div.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if columns:
                name = columns[0].text.strip()
                value = columns[1].text.strip()
                data.append((name, value))

    # Вывод извлеченных данных
    for item in data:
        print(f'Name: {item[0]}, Value: {item[1]}')

    breakpoint()

    asset_labels = ['Fixed Income (FI)',
                    'Equity (EQ)',
                    'Alternatives',
                    'Cash and/or Derivatives',
                    'North America',
                    'Europe',
                    'Asia Pacific',
                    'Latin America',
                    'World',
                    'Africa',
                    'Other',
                    'United States',
                    'United Kingdom',
                    'Japan',
                    'China',
                    'Germany',
                    'France',
                    'Canada',
                    'Switzerland',
                    'Australia',
                    'Supranational',
                    'Net Derivatives',
                    'Cash',
                    'Other',]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    asset_values = {word: 0 for word in asset_labels}
    total = 0.0
    for line in assets_text:
        for label in asset_labels:
            if label in line:
                match = re.search(r'(\d+\.\d+)%', line)
                if match:
                    asset_values[label] = float(match.group(1))
                    total += float(match.group(1))
    print(asset_values)
    print(total)
    return one_year,one_month, asset_values, OCF, date
    # return asset_values, date

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
    # print(filenames_list)
    # print(urls_list)
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

            # write_to_sheet(one_year,one_month, assets, AMC, excel_file,pdf.split('\\')[-1].split('.')[0], date)

    print('\nDone!')

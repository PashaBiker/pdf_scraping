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
import json
import requests
from requests_html import HTMLSession
# pip install requests-html

excel_file = 'BlackRock.xlsm'
excel_file = '16_milestone\BlackRock\BlackRock.xlsm'

def get_data(url):
    AMC = 0.0
    headers = {
    'authority': 'www.blackrock.com',
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

    session = HTMLSession()
    response = session.get(url, headers=headers)
    response.html.render(sleep=4, timeout=20.0)  # render the JavaScript-loaded content

    cumulative_div = response.html.find('#subTabCumulative', first=True)
    # print(cumulative_div.html)
    date = cumulative_div.find('option[selected]', first=True).text.replace('/', ' ')
    one_month = cumulative_div.find('td.oneMonth', first=True).text
    one_year = cumulative_div.find('td.oneYear', first=True).text
    three_years = cumulative_div.find('td.threeYear', first=True).text.replace('-','')
    five_years = cumulative_div.find('td.fiveYear', first=True).text.replace('-','')

    OCF = response.html.find('div.col-onch span.data', first=True).text.replace('%', '')

    try:
        AMC = response.html.find('div.col-mer span.data', first=True).text.replace('%', '')
        if AMC == '-':
            AMC = 0
    except:
        AMC = 0

    print(date)
    print(one_month)
    print(one_year)
    print(three_years)
    print(five_years)
    print(OCF)
    print(AMC)
    # print(assets_text)
    # Find all 'tr' elements within the 'tbody' tag

    # Extract all rows (tr elements) from the table
    # Parse the HTML content using Beautiful Soup
    # Iterate through each row in the table's body

    # Разбор содержимого HTML с помощью Beautiful Soup

    # Извлечение всех div-элементов с классом "fund-component column"
    # breakpoint()
    headers = {
        'authority': 'www.blackrock.com',
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

    session = HTMLSession()
    print(url)
    response = session.get(url, headers=headers)

    # Ожидание 4 секунды
    response.html.render(sleep=8, timeout=20.0)

    # Если вы хотите работать с содержимым ответа
    html_content = response.html.html

    # print(html_content)


    # Extract JSON-like strings from the HTML content
    try:
        extracted_data = []

        # Define the patterns and their corresponding replacements for "Other"    2598.53 
        patterns = {
            r'var tabsAssetclassDataTable =(\[.*?\]);': 'Other Assets',
            r'var subTabsRegionsDataTable =(\[.*?\]);': 'Other Regions',
            r'var subTabsCountriesDataTable =(\[.*?\]);': 'Other Countries'
        }

        for pattern, replacement in patterns.items():
            match = re.search(pattern, html_content)
            print(match, '--match')
            if not match:
                continue
                
            matched_string = match.group(1)
            corrected_match = re.sub(r',\s*}', '}', matched_string)
            print(corrected_match, '-- corrtected match')
            
            try:
                data_list = json.loads(corrected_match)

                for item in data_list:
                    if item.get("name") == "Other":
                        item["name"] = replacement

                extracted_data.append(data_list)
            except Exception as e:
                print(f"Error: {e}")
                continue

        # Flatten the list of lists
        flattened_data = [item for sublist in extracted_data for item in sublist]

        print(flattened_data, ' -- combined data')

        # Extract name-value pairs and compute the total sum
        name_value_pairs = [(entry.get("name"), entry.get("value")) for entry in flattened_data if "name" in entry and "value" in entry]
        asset_values = {name: float(value.replace("%", "")) for name, value in name_value_pairs}

        print(asset_values, '-- asset values')
        print(f"\nTotal Sum: {sum(asset_values.values()):.2f}")
        
    except Exception as e:
        print(e)
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
                    'Other Regions',
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
                    'Other Locations',]

        asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)
        asset_values = {word: 0 for word in asset_labels}
        
    return one_year,one_month,three_years, five_years, asset_values, OCF,AMC, date
    # return asset_values, date

def write_to_sheet(one_year,one_month,three_years, five_years, assets, OCF,AMC, spreadsheet, filename, date):

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
                cellc.number_format = '0,00%'

                celld = sheet.range('D'+str(i+1))
                celld.value = float(AMC)/100
                celld.number_format = '0,00%'

                celle = sheet.range('E'+str(i+1))
                celle.value = float(one_month)/100
                celle.number_format = '0,00%'

                cellf = sheet.range('F'+str(i+1))
                cellf.value = float(one_year)/100
                cellf.number_format = '0,00%'

                cellg = sheet.range('G'+str(i+1))
                if three_years:
                    cellg.value = float(three_years)/100
                    cellg.number_format = '0,00%'
                
                cellh = sheet.range('H'+str(i+1))
                if five_years:
                    cellh.value = float(five_years)/100
                    cellh.number_format = '0,00%'

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
                    cell.number_format = '0,00%'


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
        one_year,one_month,three_years, five_years, assets, OCF,AMC,date = get_data(url)
        write_to_sheet(one_year,one_month,three_years, five_years, assets, OCF,AMC, excel_file, filename, date)

    print('\nDone!')

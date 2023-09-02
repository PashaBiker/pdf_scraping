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

excel_file = '15_milestone\Vanguard\Vanguard.xlsm'

def get_data(url):

    if 'shares/' in url:
        base_url = url.split('shares/')[0] + 'shares/'
        # print(base_url)
        
    price_performance_url = base_url + "price-performance"
    driver = webdriver.Chrome()
    driver.get(price_performance_url)

    # Wait until the specific element appears and click the button
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/ukd-link-tabs/div/div/div/nav/button[6]'))
    element = WebDriverWait(driver, 30).until(element_present)

    button = driver.find_element(By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/ukd-link-tabs/div/div/div/nav/button[6]')
    scroll_to_past_perf = driver.find_element(By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/h3')
    driver.execute_script("arguments[0].scrollIntoView();", scroll_to_past_perf)
    time.sleep(2)  # Дайте немного времени после скролла перед тем, как кликнуть
    button.click()
    # Extract and print the table content
    table = driver.find_element(By.CLASS_NAME, 'responsive-scrollable-table')
    table_text = table.text
    one_month_one_year_text = table_text.split('\n')

    ocf = driver.find_element(By.XPATH,'//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/ukd-link-tabs/div/span')
    ocf_text = ocf.text

    date = driver.find_element(By.XPATH,'//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/p[1]')
    date_text = date.text




    # Navigate to the portfolio-data URL
    portfolio_data_url = base_url + "portfolio-data"
    driver.get(portfolio_data_url)

    # Wait until the specific element appears
    element_present_portfolio = EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-portfolio-data/ukd-underlying-allocations/div'))
    element_portfolio = WebDriverWait(driver, 30).until(element_present_portfolio)

    # Extract and print the table content
    table_portfolio = driver.find_element(By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-portfolio-data/ukd-underlying-allocations/div/div/table')
    assets_text = table_portfolio.text.split('\n')
    # Close the driver
    driver.quit()

    # print(date_text)
    date = date_text.replace("As at date ", "")
    print(date)
    # print(ocf_text)
    OCF = re.search(r'(\d+\.\d+)', ocf_text).group(1)
    print(ocf)
    # print(one_month_one_year_text[2])
    numbers = re.findall(r'[-+]?\d+\.\d+', one_month_one_year_text[2])
    one_month = numbers[0]
    one_year = numbers[3]
    print(one_month)
    print(one_year)
    # print(assets_text)

    # breakpoint()

    asset_labels = [
            'Vanguard Global Bond Index Fund GBP Hedged Acc',
	        'Vanguard FTSE Developed World ex-U.K. Equity Index Fund GBP Acc',
        	'Vanguard Global Aggregate Bond UCITS ETF GBP Hedged Accumulating',
            'Vanguard U.K. Government Bond Index Fund GBP Acc',
            'Vanguard U.K. Investment Grade Bond Index Fund GBP Acc',
            'Vanguard U.K. Inflation-Linked Gilt Index Fund GBP Acc',
            'Vanguard U.S. Government Bond Index Fund GBP Hedged Acc',
            'Vanguard U.S. Investment Grade Credit Index Fund GBP Hedged Acc',
            'Vanguard Euro Government Bond Index Fund GBP Hedged Acc',
            'Vanguard FTSE U.K. All Share Index Unit Trust GBP Acc',	
            'Vanguard Euro Investment Grade Bond Index Fund GBP Hedged Acc',	
            'Vanguard Japan Government Bond Index Fund GBP Hedged Acc',	
            'Vanguard Emerging Markets Stock Index Fund GBP Acc',	
            'Vanguard U.S. Equity Index Fund GBP Acc',
            'Vanguard S&P 500 UCITS ETF (USD) Accumulating',	
            'Vanguard FTSE Developed Europe ex-U.K. Equity Index Fund GBP Acc',	
            'Vanguard FTSE 100 UCITS ETF (GBP) Accumulating',	
            'Vanguard Japan Stock Index Fund GBP Acc',	
            'Vanguard Pacific ex-Japan Stock Index Fund GBP Acc',	
            'Vanguard USD Corporate Bond UCITS ETF GBP Hedged Acc',	
            'Vanguard FTSE 250 UCITS ETF (GBP) Accumulating',]

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

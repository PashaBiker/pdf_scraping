import os
import traceback
import PyPDF2
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
import time
# import PyPDF2
import pdfplumber
import io
import PyPDF3
from pdfminer.high_level import extract_text
import threading
from queue import Queue
import hashlib


excel_file = 'Rayner Spencer Mills Research Limited.xlsm'
folder_name = 'Rayner Spencer Mills Research Limited PDFs'


def download_worker(q, folder_name):
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

    while not q.empty():
        row_data = q.get()
        link, filename = row_data["link"], row_data["filename"]
        try:
            response = requests.get(link, params=params,
        cookies=cookies,
        headers=headers, allow_redirects=True)
            if response.status_code == 200:
                file_path = os.path.join(folder_name, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"PDF downloaded: {filename}")
            else:
                print(f"Failed to download {filename}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {filename}. Error: {e}")
        q.task_done()

def download_pdfs(spreadsheet):
    print('Downloading PDFs...')

    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets[1]

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row

    q = Queue(maxsize=0)
    for row in range(3, last_row + 1):
        link = sheet.range(f'B{row}').value
        filename = sheet.range(f'A{row}').value + '.pdf'
        q.put({"link": link, "filename": filename})

    threads = []
    num_threads = 4
    for _ in range(num_threads):
        worker = threading.Thread(target=download_worker, args=(q, folder_name))
        worker.start()
        threads.append(worker)

    # Дожидаемся завершения всех потоков
    for thread in threads:
        thread.join()

    q.join()  # Дожидаемся, пока все задания в очереди не будут обработаны

    wb.close()
    app.quit()

    print('All PDFs downloaded!')
    return folder_name

# Открываем PDF-файл
def get_charges(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Получаем вторую страницу (нумерация начинается с 0)
        page = pdf.pages[1]

        # Определяем границы для обрезки страницы (70% слева будут отброшены)
        width = page.width
        height = page.height
        left = width * 0.7  # 70% ширины страницы
        top = 0
        right = width
        bottom = height

        # Обрезаем страницу и извлекаем текст с правой части
        cropped_page = page.within_bbox((left, top, right, bottom))
        text = cropped_page.extract_text()
        text = text.split('\n')
        for line in text:
            if '(no VAT)' in line:
                DFM = re.search(r'\d.\d\d%', line).group(0).replace('%','')
                print(DFM)
            if 'KIID Ongoing Charge' in line:
                OCF = re.search(r'\d.\d\d', line).group(0).replace('%','')
                print(OCF)

    return  DFM, OCF

def get_assets(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Получаем вторую страницу (нумерация начинается с 0)
        page = pdf.pages[1]

        # Определяем границы для обрезки страницы (70% слева будут отброшены)
        width = page.width
        height = page.height
        left = 0
        top = 0
        right = width * 0.7  # 70% ширины страницы
        bottom = height * 0.5

        # Обрезаем страницу и извлекаем текст с левой части
        cropped_page = page.within_bbox((left, top, right, bottom))
        text = cropped_page.extract_text()
        text = text.split('\n')
        # print(text)

        asset_labels = ['Equities',	
        'Fixed Income',	
        'Cash/Money Market',	
        'Other',]
        asset_percentages = {}

        # Loop through each asset label and find the corresponding percentage in the text
        for asset in asset_labels:
            # Create a pattern to find the asset followed by its percentage
            pattern = rf"{asset}\s+(\d+\.\d+)"
            
            # Search the text for the pattern
            for line in text:
                match = re.search(pattern, line)
                if match:
                    # If found, add the asset and percentage to the dictionary
                    asset_percentages[asset] = float(match.group(1))

        print(asset_percentages)
        total_percentage = sum(asset_percentages.values())

        print(total_percentage)  # This will output the sum of the values
    return asset_percentages

def get_year_date(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Получаем вторую страницу (нумерация начинается с 0)
        page = pdf.pages[0]

        # Определяем границы для обрезки страницы (70% слева будут отброшены)
        width = page.width
        height = page.height
        left = 0
        top = 0
        right = width * 0.625  # 70% ширины страницы
        bottom = height

        # Обрезаем страницу и извлекаем текст с левой части
        cropped_page = page.within_bbox((left, top, right, bottom))
        text = cropped_page.extract_text()
        text = text.split('\n')
        # print(text)
        for line in text:
            if 'As of' in line:
                date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"

                # Search for the pattern in the text
                match = re.search(date_pattern, line)
                date = match.group(1)
                print(date)

            pattern = r"-?\d+\.\d+"
            matches = re.findall(pattern, line)
            # Check if there are more than three such matches
            if len(matches) > 3:
                print(f"Found line: {line}")
                # Pattern to match numbers with an optional minus, digits, a dot, and digits
                pattern = r"(-?\d+\.\d+|—)"

                # Find all matches
                matches = re.findall(pattern, line)

                # Function to convert matches to float or None
                def convert_value(value):
                    return float(value) if value != '—' else None

                # Check if we have enough values to extract the ones we are interested in
                if len(matches) >= 6:
                    one_month = convert_value(matches[0])  # The first value is the one-month value
                    one_year = convert_value(matches[2])  # The third value is the one-year value
                    three_years = convert_value(matches[3])  # The fourth value is the three-years value, here will be None
                    five_years = convert_value(matches[4]) 

                    print(one_month,
                        one_year,
                        three_years,
                        five_years,)
                break  
    return date, one_month, one_year, three_years, five_years

def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(DFM, OCF, one_month, one_year, three_years, five_years, assets, spreadsheet, filename, date):
# def write_to_sheet(OCF, management_fee, one_year, assets, spreadsheet, filename, date):

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
                if DFM is not None:
                    cellc.value = float(DFM)/100
                    cellc.number_format = '0.00%'
                
                celld = sheet.range('D'+str(i+1))
                if OCF is not None:
                    celld.value = float(OCF)/100
                    celld.number_format = '0.00%'
                
                celle = sheet.range('E'+str(i+1))
                if one_month is not None:
                    celle.value = float(one_month)/100
                    celle.number_format = '0.00%'

                cellf = sheet.range('F'+str(i+1))
                if one_year is not None:
                    cellf.value = float(one_year)/100
                    cellf.number_format = '0.00%'

                cellg = sheet.range('G'+str(i+1))
                if three_years   is not None:
                    cellg.value = float(three_years)/100
                    cellg.number_format = '0.00%'

                cellh = sheet.range('H'+str(i+1))
                if five_years   is not None:
                    cellh.value = float(five_years)/100
                    cellh.number_format = '0.00%'
                
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


def column_letter_from_index(index):
    result = ""
    while index > 0:
        index -= 1
        remainder = index % 26
        result = chr(65 + remainder) + result
        index = index // 26
    return result


if __name__ == '__main__':

    # enter the name of the excel file

# TODO UNCOMENT FIRST
# TODO UNCOMENT FIRST
# TODO UNCOMENT FIRST

    folder_name = download_pdfs(excel_file) 

    pdfs = glob.glob(folder_name + '/*.pdf')

    for pdf in pdfs:
        try:
            ''
            date, one_month, one_year, three_years, five_years = get_year_date(pdf)
            DFM, OCF = get_charges(pdf)
            asset_allocation = get_assets(pdf)
            write_to_sheet(DFM, OCF, one_month, one_year, three_years, five_years, asset_allocation, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

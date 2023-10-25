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

excel_file = '19_milestone\One Four Nine Group\One Four Nine Group.xlsm'
pdf_folder = '19_milestone\One Four Nine Group\One Four Nine Group PDFs'


def download_worker(q, folder_name):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    while not q.empty():
        row_data = q.get()
        link, filename = row_data["link"], row_data["filename"]

        response = requests.get(link, headers=headers)
        if not filename:
            filename = link.split('/')[-1]

        file_path = os.path.join(folder_name, filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"PDF downloaded: {filename}")
        q.task_done()

def download_pdfs(spreadsheet):
    print('Downloading PDFs...')

    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets[1]

    folder_name = pdf_folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row

    q = Queue(maxsize=0)
    for row in range(3, last_row+1):
        link = sheet.range(f'B{row}').value
        filename = sheet.range(f'A{row}').value + '.pdf'
        q.put({"link": link, "filename": filename})

    num_threads = 4
    for _ in range(num_threads):
        worker_thread = threading.Thread(
            target=download_worker, args=(q, folder_name))
        worker_thread.start()

    q.join()

    wb.close()
    app.quit()

    print('All PDFs downloaded!')
    return folder_name

def get_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        text = text.split('\n')

        for line in text:
            if 'AS AT' in line:
                # date_parts = line.split('AS AT: ')
                pattern = r'AS AT:\s*([\d/]+)'
                match = re.search(pattern, line)
                date = match.group(1).replace('/','.')
                print(date)

            if 'MANAGEMENT FEE' in line:
                management_fee = re.search(r'(\d+\.\d+)', line).group(1)
                print(management_fee,'MANAGEMENT FEE')
                
            if 'OCF OF UNDERLYING FUNDS' in line:
                OCF = re.search(r'(\d+\.\d+)', line).group(1)
                print(OCF, 'OCF')

        second_page = pdf.pages[1]
        text = second_page.extract_text()
        asset_text = text.split('\n')
        print(asset_text)

        
        asset_labels = ['CASH',	
                        'GOVERNMENT BOND',	
                        'INVESTMENT GRADE',	
                        'UK EQUITY',	
                        'GLOBAL EQUITY',	
                        'ASIA PACIFIC EQUITY',	
                        'EMERGING MARKETS',]

        asset_labels_pattern = "|".join(map(re.escape, asset_labels))

        assets_result = {}

        # Regular expression pattern to match percentages followed by asset labels
        pattern = r'(\d+\.?\d*)%\s*(' + asset_labels_pattern + r')'

        # Debug: Print the pattern
        # print("Pattern:", pattern)

        # Searching for matches in each line of asset_text
        for line in asset_text:
            match = re.search(pattern, line)
            if match:
                # Debug: Print the matched line
                # print("Matched Line:", line)
                # If a match is found, update the assets_result dictionary
                assets_result[match.group(2)] = float(match.group(1))

        print(assets_result)

        def extract_one_year(pdf_path):
            with pdfplumber.open(pdf_path) as pdf:
                first_page = pdf.pages[0]
                tables = first_page.extract_tables()

                # for i, table in enumerate(tables):
                    # print(f"Table {i + 1}:")
                    # for row in table:
                        # print(row)
                    # print("-" * 40)

                # Extract the desired value from the third table (index 2)
                one_year = tables[2][2][-1].replace('%','')
                print(f"one_year Value: {one_year}")
            return one_year
        
        one_year = extract_one_year(pdf_path)


    return OCF, management_fee, one_year ,assets_result,date

def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(OCF, management_fee, one_year, assets, spreadsheet, filename, date):

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
                if management_fee is not None:
                    cellc.value = float(management_fee)/100
                    cellc.number_format = '0,00%'
                
                celld = sheet.range('D'+str(i+1))
                if OCF is not None:
                    celld.value = float(OCF)/100
                    celld.number_format = '0,00%'
                
                celle = sheet.range('E'+str(i+1))
                if one_year is not None:
                    celle.value = float(one_year)/100
                    celle.number_format = '0,00%'
                
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

    pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            ''
            # OCF, management_fee, one_year ,assets_result,date = get_data(pdf)
            # write_to_sheet(OCF, management_fee, one_year, assets_result, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

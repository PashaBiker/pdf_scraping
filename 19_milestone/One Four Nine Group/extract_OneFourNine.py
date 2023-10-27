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

excel_file = 'One Four Nine Group.xlsm'
pdf_folder = 'One Four Nine Group PDFs'


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
    def safe_get(lst, index, default=None):
            return lst[index] if index < len(lst) else default

    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        first_page_text = first_page.extract_text().split('\n')
        second_page = pdf.pages[1]
        
        # Get the page's width and height
        width = second_page.width
        height = second_page.height
        
        # Calculate x1 for 59.375% of the page width
        x1 = 0.59375 * width
        
        # Define bounding box
        bbox = (0, 0, x1, height)
        
        # Crop the page
        cropped_page = second_page.crop(bbox)
        
        # Extract text from the cropped page
        second_page_text = cropped_page.extract_text().split('\n')

        # print(text)
        # print(second_page_text)
        for i,line in enumerate(first_page_text):
            if 'One Four Nine Fee' in line:
                # print(line)
                OFN_fee = re.findall(r'\d.\d\d', line)[0]
                print(OFN_fee, 'ofn fee')
            if 'Underlying Fund Fees' in line:
                # print(line)
                UF_fee = re.findall(r'\d.\d\d', line)[0]
                print(UF_fee, 'uf fee')

            if '3 Years' in line:
                numbers_line = first_page_text[i + 1]
                
                # Check if the line contains any float values. If not, get the next line.
                if not re.search(r'\d+\.\d+', numbers_line):
                    numbers_line = first_page_text[i + 2]

                numbers = re.findall(r'-?\d+\.\d+|N/A|-', numbers_line)
                print("Extracted numbers:", numbers)  # Debugging information

                # Convert numbers to float or None if 'N/A'
                numbers = [float(num) if num != 'N/A' else None for num in numbers]

                # Extract the specific values you're interested in using safe_get
                one_month = safe_get(numbers, 0)
                one_year = safe_get(numbers, 2)
                three_years = safe_get(numbers, 3)

                print(one_month,' 1m')
                print(one_year,' 1y')
                print(three_years,' 3y')

            if 'as at' in line:
                date_line = line.split('as at ')
                date = date_line[-1]
                # print(date)

        # for i,line in enumerate(second_page_text):
        #     for line in second_page_text:
        #         print()

        asset_labels_pattern = [
            'Cash',
            'UK Gilts'	,
            'International Sovereign Bonds'	,
            'Investment Grade Corporate Bonds'	,
            'High Yield Bonds'	,
            'UK Equity'	,
            'US Equity'	,
            'Japan Equity'	,
            'Europe ex UK Equity'	,
            'Asia Pacific ex Japan Equity'	,
            'Global Emerging Equity',
            'Gold',
            'Real Assets',
        ]
        asset_labels = sorted(asset_labels_pattern, key=lambda x: len(x), reverse=True)
        asset_allocation = {}

        for i, line in enumerate(second_page_text):
            # Check if a line contains a percentage value
            if "(" in line and "%" in line:
                percentage = line.split('(')[-1].split(')')[0]
                
                # Check the current line for labels
                asset_label_found = False
                for label in asset_labels:
                    if label in line:
                        asset_allocation[label] = percentage.replace('%','')
                        asset_label_found = True
                        break
                
                # If no label is found in the current line, check the previous line
                if not asset_label_found:
                    # Get combined labels from multiple lines
                    combined_previous = second_page_text[i-1]
                    combined_current = " ".join(line.split(' ')[:-1])  # Excluding the last word which contains the percentage
                    combined_label = combined_previous + " " + combined_current

                    for label in asset_labels:
                        if label in combined_label:
                            asset_allocation[label] = percentage.replace('%','')
                            break

        print(asset_allocation)

    return date, OFN_fee, UF_fee, one_month, one_year, three_years, asset_allocation

def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(OFN_fee, UF_fee, one_month, one_year, three_years, assets, spreadsheet, filename, date):
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
                if OFN_fee is not None:
                    cellc.value = float(OFN_fee)/100
                    cellc.number_format = '0.00%'
                
                celld = sheet.range('D'+str(i+1))
                if UF_fee is not None:
                    celld.value = float(UF_fee)/100
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

    # pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            ''
            date, OFN_fee, UF_fee, one_month, one_year, three_years, asset_allocation = get_data(pdf)
            write_to_sheet(OFN_fee, UF_fee, one_month, one_year, three_years, asset_allocation, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
import time
import pytesseract
from pdf2image import convert_from_path
from PIL import ImageEnhance
from concurrent.futures import ThreadPoolExecutor
import threading
import easyocr
import numpy as np


folder_name = "7_milestone\LGT\LGT PDFs"
excel_file = '7_milestone\LGT\LGT Wealth Management.xlsm'
poppler_path = r'13_milestone\AJ\poppler-23.07.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def download_pdfs(spreadsheet):
    print('Downloading PDFs...')
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets[1]

        # Create the folder if it doesn't exist 
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Start from row 3 and iterate through the links in column B
        for row in range(3, sheet.range('B3').end('down').row + 1):
            link = sheet.range(f'B{row}').value
            # Get the corresponding filename from column A
            filename = sheet.range(f'A{row}').value + '.pdf'

            try:
                # Download the PDF from the link
                response = requests.get(link)
                if response.status_code == 200:
                    # If the filename is empty or None, use the last part of the link as the filename
                    if not filename:
                        filename = link.split('/')[-1]

                    # Save the PDF in the folder
                    file_path = os.path.join(folder_name, filename)

                    # Write the content of the downloaded PDF to the file
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    print(f"PDF downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading PDF {filename}: {str(e)}")

        wb.close()
        app.quit()

        print('All PDFs downloaded!')
        return folder_name

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def ocr_from_pdf(pdf_path):
    # Convert PDF to a set of images
    images = convert_from_path(pdf_path, first_page=1, last_page=1,poppler_path=poppler_path, dpi=400)

    all_text = ""

    # Create a reader object for English language (you can add more languages if needed)
    reader = easyocr.Reader(['en'])

    for image in images:
        # Crop the image if needed
        new_width = int(image.width * (1/3))
        new_height = int(image.height * (2/3))
        cropped_image = image.crop((0, 0, new_width, new_height))

        # Convert PIL image to numpy array
        numpy_image = np.array(cropped_image)

        # Use EasyOCR to extract text from the image
        results = reader.readtext(numpy_image)

        # Concatenate the results
        picture_text = ' '.join([result[1] for result in results])

        # Apply your substitutions
        picture_text = re.sub(r'Bh Equities 1% Total', 'Bh Equities 71% Total', picture_text)
        # ... other substitutions ...

        all_text += picture_text + '\n'
        
    return all_text

def get_data(file):

    date = ''
    one_year = '0'
    one_month = '0'
    perf_labels = ['1 month', '3 month', '6 month', '1 year', '3 year', '5 year']
    perf_values = []
    filename = file.split('\\')[-1].split('.')[0]
    # if filename.startswith International MPS replace 6 month with YTD
    if filename.startswith('International MPS'):
        perf_labels[2] = 'YTD'
    performance = ''
    is_perf = False
    AMC = ''
    OCF = ''
    # print(filename)
    
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                first_line_found = False
                counter = 0
                # print(text)
                # print(text[0])
                # print(text[1])

                for line in text:
                    if 'Ongoing Charge Figure' in line or 'OCF' in line or 'Ongoing charge figure' in line:
                        OCF_Number = re.findall(r'\d+\.?\d*', line)
                        OCF = float(OCF_Number[-1])
                        # print(line)

                    if 'Annual management charge' in line:
                        AMC_Number = re.findall(r'\d+\.?\d*', line)
                        AMC = float(AMC_Number[-1])
                        date = text[2]
                        # print(line)

                    numbers = re.findall(r'[-+]?\d+\.\d+', line)
                    if len(numbers) >= 4:
                        counter += 1
                        
                    if len(numbers) >= 4 and counter == 2 and not first_line_found:
                        numbers = re.findall(r'[-+]?\d+\.\d+', line)
                        if len(numbers) > 3:
                            perf_values = numbers
                            one_month = float(numbers[0])
                            one_year = float(numbers[3])
                            first_line_found = True
                            
                    if 'Sustainable' in filename:
                        # print(line)
                        if 'Performance' in line.strip() or line.strip().endswith('As at last month end'):
                            is_perf = True
                        
                        if 'Volatility' in line.strip() and is_perf:
                            is_perf = False
                            break
                        if line.strip().endswith('%') and is_perf:
                            # print(line)
                            if 'International' in filename:
                                if len(line.split()) >4:
                                    continue
                        
                            val = line.strip().split()[-1]
                            label = line.replace(val, '').strip()
                            perf_labels.append(label)
                            perf_values.append(val)
                        
                        
                # print(date)
                # print(OCF)
                # print(AMC)
                # print(one_month)
                # print(one_year)
                if not filename.startswith('Sustainable'):
                    break
        performance = dict(zip(perf_labels, perf_values))
        # if 'International' in filename and 'Sustainable' in filename:
        # print(filename)
        # for key, value in performance.items():
        #     print(key, value)
        # print('-----------------')

    except Exception as e:
        print(f"An error occurred: {str(e)}")


    with pdfplumber.open(file) as pdf:
        text = ''

        asset_labels = ['Fixed interest',
                        'UK equity',
                        'Overseas equity',
                        'Absolute return',
                        'Infrastructure',
                        'Alternatives',
                        'Equities',
                        'Liquidity strategies',
                        'Cash',]

        asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)
        asset_values = {}

        picture = ocr_from_pdf(file)
        picture_lines = picture.split('\n')
        print(picture_lines)
        for line in picture_lines:
            for label in asset_labels:
                if label in line:
                    # Find a pattern of label followed by a number
                    match = re.search(rf'{label}\s+(\d+)', line)
                    if match:
                        asset_values[label] = match.group(1)
        # for line in picture_lines:
        #     for word in asset_labels:
        #         # Use a regular expression to find the asset word as a whole word (not as part of other words)
        #         match = re.search(r'\b' + word + r'\b', line)
        #         if match:
        #             # Extract the substring from the matched word till the end of the line
        #             substring = line[match.end():]
        #             # Use a regular expression to find the first whole number in the substring
        #             numbers = re.findall(r'\b\d+\b', substring)
        #             if numbers:
        #                 number = numbers[0]
        #                 asset_values[word] = number
        # print(asset_values)
        total = sum(int(value) for value in asset_values.values())
        
        
        
    data = {
        'Date': date,
        'Annual management charge': AMC,
        'OCF': OCF,
    }
    
    return data, performance, asset_values


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def write_to_sheet(data, performance, assets, filename, excel_file):
    print(f"Writing data of: {filename}")

    try:
        app = xw.App(visible=False)
        wb = app.books.open(excel_file, update_links=False, read_only=False)
        sheet = wb.sheets[2]

        # Find the row that matches filename
        row = next(cell.row for cell in sheet.range(
            'A:A') if cell.value == filename)

        # For every key in the data
        for key in data:
            # Find the matching column
            column = next(cell.column for cell in sheet.range(
                '1:1') if cell.value == key)

            # Write the key's value to the cell at the intersection of the row and column
            sheet.cells(row, column).value = data[key]

            if key.strip() != 'Date' and data[key]:
                value = data[key]
                if is_float(value):
                    sheet.cells(row, column).value = float(value) / 100
                    sheet.cells(row, column).number_format = '0,00%'

        column_headings = sheet.range('A1').expand('right').value

        for key in performance:
            if key not in column_headings:
                # Find the first empty column dynamically
                empty_column_index = len(column_headings) + 1
                empty_column = column_letter_from_index(empty_column_index)

                # Assign the asset value to the first empty column
                cell = sheet.range(f'{empty_column}1')
                cell.value = key

                # Append the asset to column_headings
                column_headings.append(key)

        for key in performance:
            column_index = column_headings.index(key) + 1
            cell = sheet.range(
                f'{column_letter_from_index(column_index)}{row}')
            value = performance[key].replace(',', '').replace('%', '')
            if value == '-':
                cell.value = '-'  # or some default value
            elif is_float(value):
                cell.value = float(value) / 100
            cell.number_format = '0,00%'

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

        range_values = sheet.range('A1').expand().value

        for i in range(len(range_values)):
            if filename in range_values[i]:
                for asset, value in assets.items():
                    column_index = column_headings.index(asset) + 1
                    cell = sheet.range(
                        f'{column_letter_from_index(column_index)}{i+1}')
                    if is_float(value):
                        cell.value = float(value) / 100
                    else:
                        # value = value.replace(',', '').replace('%', '')
                        cell.value = value
                    cell.number_format = '0,00%'

    except Exception as e:
        print(f"An error occurred: {str(e)}")
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


    pdf_folder = download_pdfs(excel_file) 

    pdf_folder = folder_name

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    try:
        for pdf in pdfs:
            data, performance, assets = get_data(pdf)
            filename = pdf.split('\\')[-1].split('.')[0]
            write_to_sheet(data, performance, assets, filename, excel_file)
    except Exception as e:
        print(f"An error occurred in file {pdf}: {str(e)}")
        traceback.print_exc()


    print('\nDone!')

import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
from pdfminer.high_level import extract_text
import fitz
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\Program Files\poppler-23.07.0\Library\bin'


keys = [
    'UK Equity',
    'Global Developed Equity',
    'Global Emerging Equity',
    'UK Fixed Income',
    'Property',
    'Energy & Renewables',
    'Other',
    'Fixed Income',
    'Global Developed Fixed Income',
    'Global Emerging Fixed Income',
    'Renewable Energy',
    'Alternative',
    'Cash & Money Market',
    'Commodity'
]


def get_assets(pdf_path, model_asset_pages):

    filename = pdf_path.split("\\")[-1].split(".")[0]
    print('Extracting assets of:', filename)

    page_num = model_asset_pages[filename]

    page = convert_from_path(
        pdf_path, 500, first_page=page_num, last_page=page_num, poppler_path=poppler_path)[0]
    # page = convert_from_path(
    #     pdf_path, 500, first_page=page_num, last_page=page_num)[0]

    page = np.array(page)  # Convert PIL image to numpy array

    # Extract bottom half of the page
    height, width, _ = page.shape
    roi = page[height//2:, :]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresholded_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    roi = thresholded_image

    ocr_text = pytesseract.image_to_string(roi, config='--psm 6')

    text = ocr_text.split('\n')
    print(text)
    assets = {}
    matched_keys = set()

    for line in text:
        match = re.search(
            rf'\b({"|".join(keys)})\s*(-?\d+(\.\d+)?)%\s*$', line)
        if match:
            key, val, _ = match.groups()
            if key not in matched_keys:
                matched_keys.add(key)
                assets[key] = val

    # sum_values = 0
    # for key, val in assets.items():
    #     sum_values += float(val)
    #     print(key, val)

    # print("Total:", sum_values)

    return assets


def get_pagenum_for_model(file):
    model_asset_page = {}
    doc = fitz.open(file)
    for i in range(1, len(doc), 3):
        page = doc[i]
        header_text = page.get_text().split('\n')
        if 'Responsible' in file:
            model = ''.join(header_text[-3:]).replace('-',
                                                      '').replace('Service', '').strip()
        else:
            model = header_text[-2].replace('-', '').strip()
        model_asset_page[model] = i + 1

    return model_asset_page


def download_pdfs(spreadsheet):
    print("Downloading PDFs...")
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets[1]

        # Create the folder if it doesn't exist
        folder_name = "tests\Whitechurch\Whitechurch pdfs"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Start from row 3 and iterate through the links in column B
        for row in range(3, sheet.range("B3").end("down").row + 1):
            link = sheet.range(f"B{row}").value
            # Get the corresponding filename from column A
            filename = sheet.range(f"A{row}").value + ".pdf"

            try:
                # Download the PDF from the link
                response = requests.get(link)
                if response.status_code == 200:
                    # If the filename is empty or None, use the last part of the link as the filename
                    if not filename:
                        filename = link.split("/")[-1]

                    # Save the PDF in the folder
                    file_path = os.path.join(folder_name, filename)

                    # Write the content of the downloaded PDF to the file
                    with open(file_path, "wb") as f:
                        f.write(response.content)

                    print(f"PDF downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading PDF {filename}: {str(e)}")

        wb.close()
        app.quit()

        print("All PDFs downloaded!")
        return folder_name

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_data(file):
    filename = file.split("\\")[-1].split(".")[0]
    print(f"Extracting additional data of: {filename}")

    amc = ""
    one_year = ""
    one_month = ""
    date = ""

    text = ""

    start_page = None
    end_page = None

    try:
        doc = fitz.open(file)
        for page in doc:
            text = page.get_text()
            if filename in text:
                if start_page == None:
                    start_page = page.number
                break

        # open the start page
        page = doc.load_page(start_page)
        text = page.get_text().split('\n')

        is_perf = False
        perf_keys = []
        perf_values = []

        for i, line in enumerate(text):
            if line.startswith('Data as at'):
                date = line.split('Data as at')[-1].strip()

            if line.startswith('Whitechurch Annual Management') or line.startswith('Whitechurch Annual'):
                amc = text[i+2].split('%')[0].strip()

            if line.strip() == 'Performance Table':
                is_perf = True

            if is_perf and (line.startswith('ARC') or line.startswith('BoE')):
                is_perf = False

            if is_perf:
                if line[0].isdigit() and line[-1] == 'm':
                    perf_keys.append(line)
                elif line[-1] == '%' or line.strip() == '-':
                    perf_values.append(line)
                elif line.strip().endswith('Year') or line.strip().endswith('Volatility'):
                    perf_keys.append(line+text[i+1])
                    

        one_year = perf_values[perf_keys.index(
            '0-12m')].replace('%', '').strip()
        one_month = perf_values[perf_keys.index('1m')].replace('%', '').strip()
        
        performance = dict(zip(perf_keys, perf_values))
        
        # print(len(perf_keys), len(perf_values))
        # print(perf_keys)
        # print(perf_values)

    except Exception as e:
        print(f"An error occurred in file {file}: {str(e)}")
        traceback.print_exc()

    data = {
        'Date': date,
        'Whitechurch Annual Management Fee*': amc,
    }

    return data, performance,filename


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

            if key.strip() != 'Date' and data[key].strip():
                value = data[key].replace('%', '').replace(',', '')
                if is_float(value):
                    sheet.cells(row, column).value = float(value) / 100
                    sheet.cells(row, column).number_format = '0.00%'

        column_headings = sheet.range('A1').expand('right').value
        column_headings = [str(i) for i in column_headings]
        column_headings = [heading.replace(
            '.0', '') for heading in column_headings if heading is not None]

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
                # print(column_headings)

        for key in performance:
            column_index = column_headings.index(key) + 1
            cell = sheet.range(
                f'{column_letter_from_index(column_index)}{row}')
            value = performance[key].replace(',', '').replace('%', '')
            if value == '-':
                cell.value = '-'  # or some default value
            elif is_float(value):
                cell.value = float(value) / 100
            cell.number_format = '0.00%'

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
                        value = value.replace(',', '').replace('%', '')
                        cell.value = value
                    cell.number_format = '0.00%'

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


if __name__ == "__main__":
    # enter the name of the excel file
    excel_file = "tests\Whitechurch\Whitechurch Securities Ltd.xlsm"

    # pdf_folder = download_pdfs(excel_file)
    pdf_folder = "tests\Whitechurch\Whitechurch pdfs"

    pdfs = glob.glob(pdf_folder + "/*.pdf")

    for pdf in pdfs:
        try:
            print("--------------------")
            assets = get_assets(pdf, get_pagenum_for_model(pdf))
            data, performance,filename = get_data(pdf)
            write_to_sheet(data,performance, assets, filename, excel_file)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")
            print(e)

    print("\nDone!")

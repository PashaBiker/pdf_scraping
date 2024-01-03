import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
import time
import fitz  # PyMuPDF
import threading
from queue import Queue

excel_file = 'tests/brewin_new/Brewin Dolphin.xlsm'
pdf_folder = "tests/brewin_new/Brewin Dolphin PDFs"


def get_voyager(pdf_path):
    
    def extract_names_from_right_half(pdf_path, page_number=1):
        found_labels = []
        def create_asset_label_pattern(labels):
            # Escape special characters and join the labels into a single pattern
            escaped_labels = [re.escape(label) for label in labels]
            pattern = '|'.join(escaped_labels)
            return pattern

        # List of asset labels
        asset_labels = ['Bonds', 'Alternatives', 'Cash', 'Equities – UK', 'Equities – International']
        predefined_order = {label: i for i, label in enumerate(asset_labels)}
        asset_label_pattern = create_asset_label_pattern(asset_labels)
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) > page_number:
                page = pdf.pages[page_number]  # Select the desired page (1 for second page)

                # Define a clip region for the right half of the page
                width = page.width
                height = page.height
                bbox = (width / 2, 0, width, height)

                # Extract text from the defined area
                text = page.crop(bbox).extract_text()
                if text:
                    # Regular expression to find percentages
                    found_labels = re.findall(asset_label_pattern, text)

                    # Sort the labels based on the predefined order
                    sorted_labels = sorted(found_labels, key=lambda label: predefined_order.get(label, float('inf')))

        return sorted_labels

    def extract_text_blocks(pdf_path):

        doc = fitz.open(pdf_path)
        page = doc[1]  # assuming we are extracting from the first page

        text_blocks = page.get_text("blocks")
        indexed_blocks = {index: block for index, block in enumerate(text_blocks)}

        doc.close()
        return indexed_blocks
    
    def extract_percentages(text_blocks):
        percentages = []
        for key, value in text_blocks.items():
            text = value[4]
            if "%" in text:
                lines = text.split('\n')
                for line in lines:
                    # Extract and convert each percentage value to float
                    percentage = line.strip().replace('%', '')
                    try:
                        percentages.append(float(percentage))
                    except ValueError as e:
                        # print(f"Error converting '{line}': {e}")
                        pass
        return percentages
    
    def extract_text_from_right_half(pdf_path):
        extracted_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[1]
            # Get the dimensions of the page
            width = page.width
            height = page.height

            # Define the bounding box for the right half
            # (x0, top, x1, bottom)
            bbox = (width / 2, 0, width, height)

            # Extract text from the defined area
            text = page.crop(bbox).extract_text()
            
            if text:
                extracted_text += text + "\n"
            percentages = re.findall(r'\d{1,2}\.\d+%', extracted_text)

        return percentages
    # usage

    percentages_from_text = extract_text_from_right_half(pdf_path)
    print(percentages_from_text)
    indexed_blocks = extract_text_blocks(pdf_path)

    # print(indexed_blocks)
    percentages = extract_percentages(indexed_blocks)
    print(percentages)
    # Convert list1 percentages to float

    list1_floats = [float(x.strip('%')) for x in percentages_from_text]

    # Define custom sorting key function
    def sort_key(x):
        try:
            return percentages.index(x)
        except ValueError:
            return float('inf')  # If not found, place at the end

    # Sort list1_floats based on their position in list2
    sorted_list1 = sorted(list1_floats, key=sort_key)

    # Convert back to strings with '%' if needed
    sorted_list1_str = [f'{x}%' for x in sorted_list1]


    asset_labels = extract_names_from_right_half(pdf_path)
    print(sorted_list1_str)
    print(asset_labels)
    portfolio = {label: percent.strip('%') for label, percent in zip(asset_labels, sorted_list1_str)}

    print(portfolio)
    return portfolio


def download_worker(q, folder_name):
    headers = {
        'authority': 'www.brewin.co.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'AWSALBCORS=8UUUHfQdESrvLwo4CI8XKlk6t7U9rLgG9AIoc3KGx3yFF4RezDUWtg9shBAsmI99TH33t2GzhWUDVtDbYVnL42F1APmd2Exm0ximvNvqqrsErY/Tgbw1ZidxvSd2; AWSALB=onY8tPtZa6WYnLklUHASdAq2MSKIgaXMdRTpVYucSFv4htAaZUcXwJ+tpR5oBaPVMtCRXDq/ZJPG6eDCe38mERDuEw1KXDsgyrkx2Pfg5toMszCNNv+EvB0Pycx9',
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

def get_data(file):

    Annual_management_charge = ''
    OCF = ''
    date = ''
    perf_labels = ['1 Mth', '3 Mths', '6 Mths', 'YTD',
                   '1 Yr', '2 Yrs', '3 Yrs', '4 Yrs', '5 Yrs']
    perf_values = []

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')

                print(text) 
                # breakpoint()
                tables = page.extract_tables()

                # Process each table
                for table in tables:
                    # Check if the table has more than two rows and more than five columns
                    if len(table) > 2 and all(len(row) > 5 for row in table):
                        print("Table found on page:", page.page_number)
                        main_table = table

                for line in text:
                    if 'Investment Management ' in line:
                        print(line)
                        Annual_management_charge = line.split('Management ')[
                            1].split('%')[0]
                        break

                    if 'OCF' in line:
                        # print(line)
                        OCF = line.split('OCF: ')[1]
                        # print(OCF)

                pattern1 = re.compile(r'\b\d+\.\d+\b')
                first_line_with_more_than_five_numbers = next((line for line in text if len(pattern1.findall(line)) > 5), None)

                pattern = r"-?\d+\.\d+"
                matches = re.findall(pattern, first_line_with_more_than_five_numbers)
                perf_values = matches
                print(perf_values)

                if "%" in file:
                    date = text[3]
                else:
                    date = text[1]
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # print('Annual_management_charge:', Annual_management_charge)
    # print('one_month:', one_month)
    # print('one_year:', one_year)

    asset_labels = ['Bonds', 'Equities International', 'North America',
                    'Asia', 'Dev\'d Europe ex UK', 'Japan',
                    'Emerging', 'Alternatives', 'Equities UK',
                    'Equities – UK', 'Equities – International', 'Cash', ]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    reader = PdfReader(file)
    text = ''

    # extract text from all pages
    for page in reader.pages:
        text += page.extract_text()

    # Split the extracted text into lines
    lines = text.split('\n')

    # print(lines)
    # Initialize the asset_values dictionary
    if 'Voyager' not in file:
        asset_values = {}

        for line in lines:
            for word in asset_labels:
                if word in line:
                    # Use a regular expression to find all numbers in the line
                    numbers = re.findall(r'\d+\.?\d*', line)
                    # If numbers are found, assign the last number as the value for the asset
                    if numbers:
                        # Change this to numbers[0] if the number appears before the asset name
                        number = numbers[-1]
                        asset_values[word] = number
    else:
        # asset_values = {}
        asset_values = (get_voyager(file))

    if '%' not in file:    
        performance = dict(zip(perf_labels, perf_values))
    else:
        headers = main_table[0]
        second_line = main_table[1]

        # Removing '\n' and keeping the last part of each string in headers
        cleaned_headers = [header.replace('\n', ' ') for header in headers]
        # Creating a dictionary from the cleaned headers and the second line values
        # performance = {header: value for header, value in zip(cleaned_headers, second_line)}
        
        performance_old = {header: value for header, value in zip(cleaned_headers[1:], second_line[1:])} 
        performance_old.setdefault('3 Yr', None)
        desired_keys = ['1 Mth', '3 Mths', '6 Mths', 'YTD', '1 Yr', '2 Yr', '3 Yr']
        print(performance_old)
        # Creating a new dictionary with only the desired keys and modifying 'Yr' to 'Yrs'
        # performance = {key if not key.endswith('Yr') else key.replace('Yr', 'Yrs'): performance_old[key] for key in desired_keys}
        new_dict = {
            key if key == '1 Yr' or not key.endswith('Yr') else key.replace('Yr', 'Yrs'): performance_old[key]
            for key in desired_keys
        }
        performance = new_dict
        print(performance)
        # breakpoint()
    data = {
        'Date': date,
        'AMC': Annual_management_charge,
        'OCF': OCF
    }
    
    return data, performance, asset_values


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


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

            # if key.strip() != 'Date':
            #     sheet.cells(row, column).value = float(
            #         data[key].replace('%', '').replace(',', '')) / 100
            #     sheet.cells(row, column).number_format = '0.00%'
            if key.strip() != 'Date':
                try:
                    # Remove '%' and ',' from the string and check if it's not empty
                    value_str = data[key].replace('%', '').replace(',', '')
                    if value_str.strip():
                        # Convert the cleaned string to float and divide by 100
                        sheet.cells(row, column).value = float(value_str) / 100
                        sheet.cells(row, column).number_format = '0.00%'
                    else:
                        # Set a default value for empty strings
                        sheet.cells(row, column).value = None
                        sheet.cells(row, column).number_format = '0.00%'
                except ValueError as e:
                    # Log the error and set a default value in case of conversion failure
                    print(f"Error converting '{data[key]}' to float: {e}")
                    sheet.cells(row, column).value = None
                    sheet.cells(row, column).number_format = '0.00%'

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

        # for key in performance:
        #     column_index = column_headings.index(key) + 1
        #     cell = sheet.range(
        #         f'{column_letter_from_index(column_index)}{row}')
        #     if performance[key] == '-':
        #         cell.value = '-'  # or some default value
        #     else:
        #         cell.value = float(performance[key].replace(
        #             ',', '').replace('%', '')) / 100
        #     cell.number_format = '0.00%'
        for key in performance:
            column_index = column_headings.index(key) + 1
            cell = sheet.range(f'{column_letter_from_index(column_index)}{row}')
            
            if performance[key] is None:
                # Handle the None value appropriately here
                # For example, set cell.value to '-' or some default value
                cell.value = None  # or another placeholder or default value  # or some default value
            else:
                # Assuming performance[key] is a string that might contain commas or percent signs
                value = performance[key].replace(',', '').replace('%', '')
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
                    cell.value = float(value.replace(
                        ',', '').replace('%', '')) / 100
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


if __name__ == '__main__':

    # TODO: comment it
    # TODO: comment it
    # TODO: comment it

    # pdf_folder = download_pdfs(excel_file)

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            print('---------------')
            data, performance, asset_values = get_data(pdf)
            filename = pdf.split('\\')[-1].split('.')[0]
            write_to_sheet(data, performance, asset_values,
                           filename, excel_file)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

import glob
import PyPDF2
import pdfplumber
import xlwings as xw
import requests
import os
import re
import traceback
# pip install PyMuPDF
import fitz  # PyMuPDF
import re
import pdf2image
from PIL import Image
import pytesseract
import os
import threading
from queue import Queue
import hashlib

excel_file = 'Trust DFM.xlsm'
pdf_folder = 'Trust DFM PDFs'

def get_data_addition(pdf):
    def extract_top_left_text(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            
            # Use enumerate to get the page index
            for i, page in enumerate(pdf.pages):
                # Check if the page is one of 1, 4, 8, etc. (keeping in mind that indices start from 0)
                if (i+1) % 4 != 1:
                    continue

                # Calculate dimensions for the top-left quadrant
                x0, top, x1, bottom = page.bbox
                width = x1 - x0
                height = bottom - top

                crop_box = (x0, top, x0 + width * 0.5, top + height * 0.5)
                
                # Crop the page to the top-left quadrant and extract text
                cropped_page = page.crop(bbox=crop_box)
                all_text += cropped_page.extract_text() + "\n"

        return all_text.strip().split('\n')

    # Example
    text = extract_top_left_text(pdf)

    assets_categories = ['Equity', 'Fixed Income', 'Cash', 'Multi Asset ', 'Alternatives']
    assets_groups = []
    assets_current_group = []
    found_assets_holdings = False

    for i, line in enumerate(text):
        if 'ASSET CLASS' in line :
            found_assets_holdings = True
            continue  # Пропускаем текущую строку, чтобы она не добавлялась в current_group

        # Если находим строку 'Important Information', останавливаем добавление
        elif 'OBJECTIVES AND POLICY' in line:
            found_assets_holdings = False
            
            if assets_current_group:
                assets_groups.append(assets_current_group)
                # print(groups)
                assets_current_group = []

        # Если мы внутри интересующего нас блока, добавляем строки
        elif found_assets_holdings:
            assets_current_group.append(line.strip())
        assets_categories_pattern = "|".join(assets_categories)

        assets_result = []
    # print(current_group)
    for group in assets_groups:
        i = 0
        while i < len(group):
            if i < len(group) - 1 and "Fixed Income Multi Asset" in group[i] and group[i + 1] == "Credit":
                percentage_part = group[i].split('Fixed Income Multi Asset ')[1]
                group[i] = 'Fixed Income Multi Asset Credit ' + percentage_part
                group.pop(i + 1)
            i += 1  
            
    # print(groups, '-- groups \n')
    for lst in assets_groups:
        category_values = []
        # Сombine all in one string
        joined_string = " ".join(lst)
        # Ищем все вхождения категорий в объединенной строке
        for match in re.finditer(assets_categories_pattern, joined_string):
            category = match.group(0)  # Получаем название категории
            # Получаем подстроку после найденной категории
            string_after_category = joined_string[match.end():]
            # Ищем первое число в подстроке (значение категории)
            value_match = re.search(r'\b\d+(\.\d+)?', string_after_category)
            if value_match:
                value = value_match.group(0)  # Получаем значение
                # Добавляем категорию и значение в список
                category_values.append(f"{category} {value}%")
        assets_result.append(category_values)

    for i in range(len(assets_result)):
        assets_result[i] = list(dict.fromkeys(assets_result[i]))
    # print('\n'*2, result, '-- result \n')
    assets_grouped_assets = []
    for group in assets_result:
        keys = []
        values = []
        for line in group:
            key, value = line.rsplit(' ', 1)  # Разделяем строку на две части по последнему пробелу
            keys.append(key)
            values.append(value)
        assets = dict(zip(keys, values))
        assets_grouped_assets.append(assets)
    return assets_grouped_assets

def get_data(file):


    filenames = []
    date = []
    ongoing_costs = []
    one_month = []
    one_year = []

    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text(use_text=True)
        text = text.split('\n')
        # print(text)
        # breakpoint()
        for i, line in enumerate(text):
            if i == 0:
                filenames.append(text[0])
            elif i == len(text) - 1:
                continue
            else:
                if '4 of 4' in line:
                    filenames.append(line.split('4 of 4')[-1].strip())

        # print(filenames)
        for i,line in enumerate(text):
            if 'Ongoing Costs' in line:
                oc_match = re.search(r'(\d+\.\d+)', line)
                ongoing_costs.append(float(oc_match.group(1))/100)
                date.append(text[1])
            if "Time Period" in line:
                # print(text[i+1])
                values_line = text[i+1]
                values = re.findall(r'(-?\d+\.\d+)%', values_line)
                one_month.append(float(values[0])/100)
                one_year.append(float(values[3])/100)
            

    print(filenames)
    print(date)
    print(ongoing_costs)
    print(one_month)
    print(one_year)

    unsorted_categories = [
        'Global Equities',
        'Corporate Bonds',
        'Global Multi Asset',
        'UK Equities',
        'Cash',
        'Alternatives',
        'Asia Pacific Ex Japan Equities',
        'European Equities',
        'Fixed Income Multi Asset',
        'Fixed Income Multi Asset Credit',
        'Japanese Equities',   
        'Emerging Market Equities',
        'Global Government Bonds',
        'US Equities',
    ]

    categories = sorted(unsorted_categories, key=lambda x: len(x), reverse=True)

    groups = []
    current_group = []
    found_portfolio_holdings = False

    for i, line in enumerate(text):
        if 'WEIGHTS BY ASSET' in line :
            found_portfolio_holdings = True
            continue  # Пропускаем текущую строку, чтобы она не добавлялась в current_group

        # Если находим строку 'Important Information', останавливаем добавление
        elif 'TOP 10 PERFORMANCE CONTRIBUTORS OVER 1 YEAR' in line:
            found_portfolio_holdings = False
            
            if current_group:
                groups.append(current_group)
                # print(groups)
                current_group = []

        # Если мы внутри интересующего нас блока, добавляем строки
        elif found_portfolio_holdings:
            current_group.append(line.strip())
        categories_pattern = "|".join(categories)

        result = []
    # print(current_group)
    for group in groups:
        i = 0
        while i < len(group):
            if i < len(group) - 1 and "Fixed Income Multi Asset" in group[i] and group[i + 1] == "Credit":
                percentage_part = group[i].split('Fixed Income Multi Asset ')[1]
                group[i] = 'Fixed Income Multi Asset Credit ' + percentage_part
                group.pop(i + 1)
            i += 1  
            
    # print(groups, '-- groups \n')
    for lst in groups:
        category_values = []
        # Сombine all in one string
        joined_string = " ".join(lst)
        # Ищем все вхождения категорий в объединенной строке
        for match in re.finditer(categories_pattern, joined_string):
            category = match.group(0)  # Получаем название категории
            # Получаем подстроку после найденной категории
            string_after_category = joined_string[match.end():]
            # Ищем первое число в подстроке (значение категории)
            value_match = re.search(r'\b\d+(\.\d+)?', string_after_category)
            if value_match:
                value = value_match.group(0)  # Получаем значение
                # Добавляем категорию и значение в список
                category_values.append(f"{category} {value}%")
        result.append(category_values)

    for i in range(len(result)):
        result[i] = list(dict.fromkeys(result[i]))
    # print('\n'*2, result, '-- result \n')
    grouped_assets = []
    for group in result:
        keys = []
        values = []
        for line in group:
            key, value = line.rsplit(' ', 1)  # Разделяем строку на две части по последнему пробелу
            keys.append(key)
            values.append(value)
        assets = dict(zip(keys, values))
        grouped_assets.append(assets)

    print(grouped_assets)


    def merge_lists(list1, list2):
        # Initialize an empty list to store the merged dictionaries
        merged_list = []

        # Loop over pairs of dictionaries from list1 and list2
        for dict1, dict2 in zip(list1, list2):
            # Create a copy of the dictionary from list1 to avoid modifying the original
            merged_dict = dict1.copy()
            
            # Update the merged dictionary with key-value pairs from dict2, only if the key doesn't exist in dict1
            for key, value in dict2.items():
                if key not in merged_dict:
                    merged_dict[key] = value

            # Add the merged dictionary to the merged list
            merged_list.append(merged_dict)

        return merged_list
    
    assets_grouped_assets = get_data_addition(file)
    combined_list = merge_lists(assets_grouped_assets, grouped_assets)
    print(combined_list)
    result2 = {}
    for i, filename  in enumerate(filenames):
        result2[filename] = {
            'Date': date[i],
            'Ongoing Costs*': ongoing_costs[i],
            '1yr': one_year[i],
            '1m': one_month[i],
            'Assets': combined_list[i]
        }
        print(
            'Date', date[i], "\n",
            'One month', one_month[i],"\n",
            '12 months', one_year[i],"\n",
            'Ongoing Costs', ongoing_costs[i],"\n",
            'Assets', combined_list[i],"\n",
            )
    # print(result)
    
    return result2


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

def write_to_sheet(data, excel_file):

    try:
        app = xw.App(visible=False)
        wb = app.books.open(excel_file, update_links=False, read_only=False)
        # breakpoint()
        for filename, values in data.items():
            print('Writing data of', filename)
            # Find the row that matches filename
            sheet = wb.sheets[2]

            row = None
            for cell in sheet.range('A:A'):
                if cell.value and cell.value.strip() == filename.strip():
                    row = cell.row
                    break

            if row is None:
                print(f"Filename '{filename}' not found in the sheet.")
                continue

            for key in values:
                if key == 'Assets':
                    continue

                # Find the matching column
                column = None
                for cell in sheet.range('1:1'):
                    if cell.value and cell.value.strip() == key.strip():
                        column = cell.column
                        break

                if column is None:
                    print(f"Column '{key}' not found in the sheet.")
                    continue

                # Write the key's value to the cell at the intersection of the row and column
                sheet.cells(row, column).value = values[key]

            sheet = wb.sheets[3]

            column_headings = sheet.range('A1').expand('right').value

            for asset, value in values['Assets'].items():
                if asset not in column_headings:
                    sheet.range(
                        f'{column_letter_from_index(len(column_headings)+1)}1').value = asset
                    # Update the column_headings list after adding the new column
                    column_headings = sheet.range('A1').expand('right').value

            for asset, value in values['Assets'].items():
                column_index = column_headings.index(asset) + 1
                cell = sheet.range(
                    f'{column_letter_from_index(column_index)}{row}')
                cell.value = float(value.replace('%','')) / 100
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

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash in chunks for large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

if __name__ == '__main__':

    pdf_folder = download_pdfs(excel_file)

    pdfs = glob.glob(pdf_folder + '/*.pdf')
    # Calculate hashes for all PDFs
    hashes = {pdf: calculate_sha256(pdf) for pdf in pdfs}

    # Group PDFs by their hashes
    grouped_pdfs = {}
    for pdf, pdf_hash in hashes.items():
        if pdf_hash not in grouped_pdfs:
            grouped_pdfs[pdf_hash] = []
        grouped_pdfs[pdf_hash].append(pdf)

    # From each group of identical PDFs, remove all but one stay
    for pdf_group in grouped_pdfs.values():
        for pdf in pdf_group[1:]:
            os.remove(pdf)

    for file in pdfs:

        try:
            data = get_data(file)
            write_to_sheet(data, excel_file)

        except Exception as e:
            print(f"Error while processing {file}: {str(e)}")
            traceback.print_exc()

    print('\nDone!')

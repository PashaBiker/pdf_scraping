import glob
import pdfplumber
import xlwings as xw
import requests
import os
import re
import traceback
import hashlib

excel_file = '8_milestone\Morningstar\Morningstar Investment Management Europe Limited.xlsm'
pdf_folder = '8_milestone\Morningstar\Morningstar PDFs'


def get_data(file):

    date = []
    charge = []
    one_year = []
    one_month = []
    perf_labels_list = []
    perf_values_list = []

    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages[1:-1]:
            text += page.extract_text()
        counter = 0
        text = text.split('\n')
        # print('text got')
        # print(text)
        # search_for_one_year = False
        for i, line in enumerate(text):

            if 'Annual Management Charge' in line:
                charge_value = re.search(r'(\d+\.\d+)%', line)
                charge.append(charge_value.group(1))
                date_match1 = re.search(r'Factsheet\s+(\d{2}/\d{2}/\d{4})', text[1])
                if date_match1:
                    date_value1 = date_match1.group(1)
                    modified_date1 = date_value1.replace('/', '.')
                    date.append(modified_date1)
                else:
                    # Если в первой строке даты нет, проверяем вторую строку
                    date_match2 = re.search(r'(\d{2}/\d{2}/\d{4})', text[2])
                    if date_match2:
                        date_value2 = date_match2.group(1)
                        modified_date2 = date_value2.replace('/', '.')
                        date.append(modified_date2)

            numbers = re.findall(r'-?\d+\.\d+', line)
            
            if 'Trailing Returns %' in line:
                line = line.split('Trailing Returns %')[1].split('Inception')[0].split()
                if line[-1] == 'Since':
                    line[-1] = 'Since Inception'
                perf_labels_list.append(line)
            
            if len(numbers) >= 3:
                
                if len(numbers) >= len(perf_labels_list[-1]):
                    perf_values_list.append(numbers)
                # print(numbers)
                
                if counter % 2 == 0:
                    one_month.append(float(numbers[0])/100)
                else:
                    one_year.append(float(numbers[0])/100)
                counter += 1

        print(date)
        print(charge)
        print(one_year)
        print(one_month)

    text = ''

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[1:-1]:
            text += page.extract_text()

    text = text.split('\n')
    # text = [line for line in text if line.strip() != '']

    # print(text)
    prev_portfolio = ""
    filenames = []

    found_portfolio_holdings = False
    groups = []
    current_group = []

    for i, line in enumerate(text):
        line = re.sub(r'\d+\.\d{1,2}%', '', line)
        if i == 0:
            continue
        elif i == len(text) - 1:
            continue
        else:

            if 'All rights reserved. For Financial Advisers and their Clients using' in line:
                # print(line)
                portfolio_match = re.search(r'Portfolios\.([\w\s–\-]+) ß', line)
                if portfolio_match:
                    current_portfolio = portfolio_match.group(1).strip().replace(" ß®", "").replace(" ß", "")  
                    if current_portfolio != prev_portfolio and current_portfolio not in filenames:
                        filenames.append(current_portfolio)
                        prev_portfolio = current_portfolio
                        
            # Если находим строку 'Asset Allocation', начинаем добавление
            if 'Asset Allocation' in line:
                found_portfolio_holdings = True
                continue  # Пропускаем текущую строку, чтобы она не добавлялась в current_group

            # Если находим строку 'Important Information', останавливаем добавление
            elif 'Returns Disclosure' in line:
                found_portfolio_holdings = False

                if current_group:
                    groups.append(current_group)
                    current_group = []

            # Если мы внутри интересующего нас блока, добавляем строки
            elif found_portfolio_holdings:
                current_group.append(line.strip())

    print(filenames)
    # print(groups)

    categories = [
        'Fixed Income',
        'Equity',
        'Cash & Cash Equivalents',
        'GBP Corporate Bond',
        'UK Equity',
        'Global High Yield Bond',
        'Other Bond',
        'Global Emerging Markets Bond',
        'Global Corporate Bond',
        'UK Gilts',
        'Global Equity',
        'China Equity',
        'Global Inflation-Linked Bond',
        'North American Equity',
        'Asia Dev ex Japan Equity',
        'Japan Equity',
        'Other Equity',
        'Property',
        'European Equity',
        'Global Bond',
        'Emerging Markets Equity',
        'UK Inflation-Linked Bond',
        ]

    sorted_categories = sorted(categories, key=len, reverse=True)
    # categories_pattern = "|".join(sorted_categories)

    result = []
    grouped_assets = []

    for group in groups:
        asset_values = {}
        lines_to_check = list(group)  # Создаем копию списка строк для проверки
        for category in sorted_categories:
            for line in lines_to_check:
                if re.search(r'\b' + re.escape(category) + r'\b', line):
                    value_match = re.search(r'(\d+\.\d{1,2})', line)
                    if value_match:
                        asset_values[category] = value_match.group(1)  # добавляем знак % к строке
                    lines_to_check.remove(line)  # Удаляем строку из дальнейшего рассмотрения
                    break
        grouped_assets.append(asset_values)
    # print(result)

    data = {}

    for i, filename in enumerate(filenames):
        data[filename] = {
            'Date': date[i],
            '1Y': one_year[i],
            '1Month': one_month[i],
            'Annual Management Charge': charge[i],
        }
        
        performance = dict(zip(perf_labels_list[i], perf_values_list[i]))
        
        write_to_sheet(data[filename], performance, grouped_assets[i], filename, excel_file)
        print(
            'date', date[i], '\n',
            '12 months', one_year[i], "\n",
            '1 month', one_month[i], "\n",
            'Annual Management Charge', charge[i], "\n",
            'Assets', grouped_assets[i], "\n",
        )

    return data


def download_pdfs(spreadsheet):
    print('Downloading PDFs...')
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets[1]

        # Create the folder if it doesn't exist
        folder_name = pdf_folder
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Start from row 3 and iterate through the links in column B
        last_row = sheet.range(
            'B' + str(sheet.cells.last_cell.row)).end('up').row
        for row in range(3, last_row+1):
            link = sheet.range(f'B{row}').value
            print(link)
            # Get the corresponding filename from column A
            filename = sheet.range(f'A{row}').value + '.pdf'

            try:
                # Download the PDF from the link
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
                response = requests.get(link, headers=headers)
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
                    sheet.cells(row, column).number_format = '0,00%'

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
                        value = value.replace(',', '').replace('%', '')
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

    # pdf_folder = download_pdfs(excel_file)

    pdfs = glob.glob(pdf_folder + '/*.pdf')
    # Calculate hashes for all PDFs
    hashes = {pdf: calculate_sha256(pdf) for pdf in pdfs}

    # Group PDFs by their hashes
    grouped_pdfs = {}
    for pdf, pdf_hash in hashes.items():
        if pdf_hash not in grouped_pdfs:
            grouped_pdfs[pdf_hash] = []
        grouped_pdfs[pdf_hash].append(pdf)

    # From each group of identical PDFs, remove all but one
    for pdf_group in grouped_pdfs.values():
        for pdf in pdf_group[1:]:
            os.remove(pdf)

    for file in pdfs:

        try:
            print(file)
            data = get_data(file)

        except Exception as e:
            print(f"Error while processing {file}: {str(e)}")
            traceback.print_exc()

    print('\nDone!')

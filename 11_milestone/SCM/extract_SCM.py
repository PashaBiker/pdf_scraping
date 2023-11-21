import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
import time

excel_file = '11_milestone\SCM\SCM Private.xlsm'
pdf_folder = '11_milestone\SCM\SCM PDFs'


def download_pdfs(spreadsheet):
    print('Downloading PDFs...')

    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets[1]

    # Create the folder if it doesn't exist
    folder_name = pdf_folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Start from row 3 and iterate through the links in column B
    last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row
    for row in range(3, last_row+1):
        link = sheet.range(f'B{row}').value
        print(link)
        # Get the corresponding filename from column A
        filename = sheet.range(f'A{row}').value + '.pdf'
        print(filename)
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
        # If the filename is empty or None, use the last part of the link as the filename
        if not filename:
            filename = link.split('/')[-1]

        # Save the PDF in the folder
        file_path = os.path.join(folder_name, filename)

        # Write the content of the downloaded PDF to the file
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"PDF downloaded: {filename}")

    wb.close()
    app.quit()

    print('All PDFs downloaded!')
    return folder_name


def get_data(file):

    date = ''
    
    perf_labels = ['Last Month','YTD' ,'Last 3 Yrs','Last 5 Yrs','Since Inception']
    perf_values = []

    try:
        with pdfplumber.open(file) as pdf:
            first_month_found = False
            first_year_found = False
            for page in pdf.pages:
                width = page.width  # Получение ширины страницы

                # Определение координат для обрезки правой половины страницы
                # (x0, y0, x1, y1)
                cropped_area = (width / 2, 0, width, page.height)
                cropped_page = page.crop(bbox=cropped_area)  # Обрезка страницы

                # Извлечение текста из обрезанной страницы
                text = cropped_page.extract_text()
                text = text.split('\n')
                # print(text)
                date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{2}')
                one_month_line = None
                one_year_line = None
                one_month = 0
                for i, line in enumerate(text):
                    if 'Rolling Return' in line:

                        label = '12m to '+text[i+2].split()[-1]
                        perf_labels.insert(0, label)
                        val = text[i+3].split()[-1]
                        perf_values.insert(0, val)
                    if 'As at' in line:
                        # Поиск даты
                        date_match = re.search(
                            r'(\d{1,2})(?:st|nd|rd|th)?\s(\w+)\s(\d{4})', line)
                        if date_match:
                            # Составление даты без суффиксов
                            date = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}"

                    if 'Management Charge' in line:
                        AMC_number = re.findall(r'\d+\.?\d*', line)
                        AMC = AMC_number[0]

                    if 'Ongoing Charge' in line:
                        OCF_Number = re.findall(r'\d+\.?\d*', line)
                        OCF = OCF_Number[0]
                        # print(line)

                    if 'Last Month' in line:
                        numbers = re.findall(r'[-+]?\d+\.\d+', text[i+1])
                        if len(numbers) >= 4 and not first_month_found:
                            
                            one_month = numbers[0]
                            # Сохраняем текущую строку
                            one_month_line = text[i+1]
                            first_month_found = True

                    if date_pattern.search(line):
                        continue

                    numbers = re.findall(r'[-+]?\d+\.\d+', line)

                    # Проверяем, что текущая строка отличается от one_month_line
                    if len(numbers) >= 3 and not first_year_found and line != one_month_line:
                        # print(line)
                        one_year = numbers[-1]
                        one_year_line = line  # Сохраняем текущую строку
                        first_year_found = True
                        
                    if any(label in line for label in perf_labels):
                        
                        perf_values = (text[i+1].replace('Inception','')+text[i+2]).split()

                # print(date)
                # print(AMC)
                # print(OCF)
                # print(one_year)
                # print(one_month)

                break
            
        perfomance = dict(zip(perf_labels, perf_values))

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Bonds',
                    'Equities',
                    'Cash',
                    'United Kingdom',
                    'North America',
                    'Japan',
                    'Asia emrg',
                    'Europe dev',
                    'Asia dev',
                    'Africa / Middle East',
                    'Latin America',
                    'Europe emrg',
                    'Australasia', ]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    with pdfplumber.open(file) as pdf:
        text = ''

        # extract text from all pages
        for page in pdf.pages:
            width = page.width  # Получение ширины страницы

            # Определение координат для обрезки левой половины страницы
            cropped_area = (0, 0, width / 2, page.height)  # (x0, y0, x1, y1)
            cropped_page = page.crop(bbox=cropped_area)  # Обрезка страницы

            # Извлечение текста из обрезанной страницы
            text += cropped_page.extract_text()

        # Split the extracted text into lines
        lines = text.split('\n')
        # print(lines)
        # Initialize the asset_values dictionary
        asset_values = {word: '0' for word in asset_labels}

        start_processing = False
        end_processing = False
        total = 0.0
        for line in lines:
            if 'Overall Asset Allocation' in line:
                start_processing = True
            if 'Fixed Income By Region' in line or 'Performance is based' in line:
                start_processing = False

            if start_processing:
                for word in asset_labels:
                    pattern = r'{}\s*(\d+\.?\d*)%'.format(word)
                    numbers = re.findall(pattern, line)
                    if numbers:
                        number = numbers[0]
                        asset_values[word] = number
                        # total += float(number)

        # print(total)
        # print(asset_values)
        # print('\n'*3)
        
        
    data = {
        'Date': date,
        'SCM Discretionary Fund Management Charge': AMC,
        'Underlying ETF costs (KIID Ongoing Charge)': OCF,
    }
    
    return data, perfomance, asset_values


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

            if key.strip() != 'Date' and data[key].strip():
                value = data[key].replace('%', '').replace(',', '')
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

    # enter the name of the excel file

    # TODO UNCOMENT FIRST
    # TODO UNCOMENT FIRST
    # TODO UNCOMENT FIRST

    pdf_folder = download_pdfs(excel_file)

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            data, performance, assets = get_data(pdf)
            filename = pdf.split('\\')[-1].split('.')[0]
            write_to_sheet(data, performance, assets, filename, excel_file)
        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")


    print('\nDone!')

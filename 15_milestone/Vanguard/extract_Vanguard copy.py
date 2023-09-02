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

excel_file = '15_milestone\Vanguard\Vanguard.xlsm'
pdf_folder = 'Vanguard PDFs'

def get_data(url):

    if 'shares/' in url:
        base_url = url.split('/shares/')[0] + '/shares/'
        print(base_url)
    breakpoint()
    date = ''
    AMC = None
    first_line_found = False
    one_year = None
    one_month = None
    try:
        with pdfplumber.open(file) as pdf:
            first_line_found = False
            first_AMC_found = False
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                # print(text)

                for line in text:

                    if 'as at' in line:
                        # print(line)
                        date_match = re.search(r'(\d{1,2}\s\w+\s\d{4})', line)
                        if date_match:
                            date = date_match.group(1)

                    if 'Class B GBP' in line:
                        # print(line)
                        AMC_number = re.findall(r'\d+\.?\d*', line)
                        AMC = AMC_number[1]

                    if 'DISCRETE ANNUAL PERFORMANCE' in line:
                        first_line_found = True
                        continue

                    if first_line_found:
                        # Проверка на отсутствие даты в строке
                        if not re.search(r'\d+\.\d+\.\d+', line):
                            # Поиск чисел с десятичной точкой
                            numbers = re.findall(r'[-+]?\d+\.\d+', line)
                            if len(numbers) >= 4:
                                if one_year is None:
                                    one_year = numbers[0]
                                elif one_month is None:
                                    one_month = numbers[0]

            # print(date)
            # print(AMC)
            # print(one_year)
            # print(one_month)


    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Equities',
                    'Fixed Income',
                    'Diversifiers',

                    'Global STAR Equities',
                    'North American',
                    'Europe ex UK',
                    'UK',
                    'Equity Themes',
                    'Emerging Markets',

                    'Government & Supranational',

                    'Corporate Senior',
                    'Corporate Subordinated',

                    'Financials Senior',
                    'Financials Subordinated',
                    'Cash/derivatives',

                    'Alternative Funds',
                    'Cash',
                    'Gold',
                    'Commodities',]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 0:  # Если это первая страница
                # Обрезать верхнюю половину по высоте и 62.5% левой части по ширине
                right_bottom_quarter = page.crop((page.width * 0.625, page.height / 2, page.width, page.height))
                text = right_bottom_quarter.extract_text()
                
                # Разделяем текст на строки и добавляем их в список
                lines = text.split('\n')

            elif i == 1:  # Если это вторая страница
                # Обрезать 37.5% левой стороны страницы
                right_part = page.crop((page.width * 0.375, 0, page.width, page.height))
                text = right_part.extract_text()
                
                # Разделяем текст на строки и добавляем их в список
                lines.extend(text.split('\n'))
            else:
                # Если страниц больше двух, завершите цикл
                break
        print(lines)
        # Initialize the asset_values dictionary
        asset_values = {word: 0 for word in asset_labels}
        lines_to_remove = []
        total = 0.0
        for line in lines:
            matched = False
            # Для каждой метки актива в asset_labels проверяем, содержится ли она в строке
            for label in asset_labels:
                if label in line:
                    # Если содержится, то используем регулярное выражение, чтобы извлечь числовое значение
                    value = re.search(r'(\d+\.\d+)', line.replace(label, ''))  # удаляем метку, чтобы избежать конфликтов
                    if value:
                        asset_values[label] = float(value.group(1))
                        total += float(value.group(1))
                        matched = True
                        lines_to_remove.append(line)
                        break
            if matched:
                asset_labels.remove(label)
        
        # Удаляем обработанные строки
        for line in lines_to_remove:
            lines.remove(line)
        categories = ["Corporate", "Financials"]
        current_category = None

        for i, line in enumerate(lines):
            for category in categories:
                if category in line:
                    current_category = category

            if "Senior" in line:
                value = re.search(r'(\d+\.\d+)', line)
                if value:
                    key = f"{current_category} Senior"
                    asset_values[key] = float(value.group(1))

            if "Subordinated" in line:
                value = re.search(r'(\d+\.\d+)', line)
                if value:
                    key = f"{current_category} Subordinated"
                    asset_values[key] = float(value.group(1))    
        print(asset_values)
        print(total)
 
    return one_year,one_month, asset_values, AMC, date
    # return asset_values, date

def write_to_sheet(one_year,one_month, assets, AMC, spreadsheet, filename, date):

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
                cellc.value = float(AMC)/100
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

    for filename in filenames:
        for url in urls:
            one_year,one_month, assets, AMC, date = get_data(url)
            write_to_sheet(one_year,one_month, assets, AMC, excel_file,filename, date)
            # write_to_sheet(one_year,one_month, assets, AMC, excel_file,pdf.split('\\')[-1].split('.')[0], date)

    print('\nDone!')

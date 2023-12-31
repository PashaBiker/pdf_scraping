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
import PyPDF2
import pdfplumber

excel_file = 'Brooks Macdonald.xlsm'
pdf_folder = 'Brooks PDFs'

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
    AMC = 0.0
    OCF = 0.0
    first_line_found = False
    one_year = 0.0

    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text(use_text=True)

        text = text.split('\n')
        print(text)
        for line in text[:5]:
                match = re.search(r'\d{2}\.\d{2}\.\d{4}', line)
                if match:
                    date = match.group()

        for i, line in enumerate(text):
            if 'Annual management charge' in line:
                for offset in range(0, 2):  # check other lines
                    if i + offset < len(text):  # check if line is exist
                        founded_line = text[i+offset].strip()
                        if re.search(r'\d+\.\d+%', founded_line):  # if pattern found
                            perscent_pattern = r'\d+\.\d+%'
                            AMC = re.findall(perscent_pattern, founded_line)[0].replace('%','')

            if 'OCF ' in line:
                parts = line.split('%')  # split by '%'
                OCF = parts[0].strip().split()[1]  # take only first part and then add '%'
            
            if '3M 6M 1Y 3Y 5Y' in line:
                for offset in range(1, 4):  # check other lines
                    if i + offset < len(text):  # check if line is exist
                        founded_line = text[i + offset].strip()
                        matches = re.findall(r'[+-]?\d+\.\d+', founded_line)
                        print(founded_line)
                        if len(matches) >= 3 and first_line_found == False:
                            cleaned_line = re.sub(r'.*?(MPS.*)', r'\1', founded_line)
                            numbers = re.findall(r'[+-]?\d+\.\d+', cleaned_line)
                            one_year = float(numbers[2])
                            first_line_found =True
        print(date)
        print(AMC)
        print(OCF)
        print(one_year)
        if one_year == 0.0:
            reader = PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text()
            text = text.split('\n')
            print(text)
            first_line_found = False

            one_year = 0.0
            for i, line in enumerate(text):
                if '3M 6M 1Y 3Y 5Y' in line:
                    for offset in range(1, 4):  # check other lines
                        if i + offset < len(text):  # check if line is exist
                            founded_line = text[i + offset].strip()
                            matches = re.findall(r'[+-]?\d+\.\d+', founded_line)
                            print(founded_line)
                            if len(matches) >= 3 and first_line_found == False:
                                cleaned_line = re.sub(r'.*?(MPS.*)', r'\1', founded_line)
                                numbers = re.findall(r'[+-]?\d+\.\d+', cleaned_line)
                                one_year = float(numbers[2])
                                first_line_found =True

            print(one_year)

    categories = ["UK Fixed Interest", "International Fixed Interest", "UK Equities", "North American Equities",
        "European Equities", "Japan/Far East/Emerging","International & Thematic Equities", 
        "Hedge Funds & Alternatives", "Structured Return", "Cash", "Property"]
    with pdfplumber.open(file) as pdf:
        text = ''
        
        for i, page in enumerate(pdf.pages):
            
            # Если это вторая страница, обрежем ее
            if i == 1:
                start_crop = page.width * 0.3
                end_crop = start_crop + (page.width * 0.625) - start_crop
                
                # Обрезка страницы с учетом начальной и конечной точки
                page = page.crop((start_crop, 0, end_crop, page.height))
            
            text += page.extract_text()

        text = text.split('\n')

    # print(text)
    joined_text = " ".join(text)

    category_values = []

    categories_pattern = "|".join(categories)
    for match in re.finditer(categories_pattern, joined_text):
        category = match.group(0)  # Получаем название категории
        # Получаем подстроку после найденной категории
        string_after_category = joined_text[match.end():]
        # Ищем первое число в подстроке (значение категории)
        value_match = re.search(r'\b\d+(\.\d+)?%', string_after_category)
        if value_match:
            value = value_match.group(0)  # Получаем значение
            # Добавляем категорию и значение в список
            category_values.append(f"{category} {value}")

    grouped_assets = {}
    for line in category_values:
        key, value = line.rsplit(' ', 1)  # Разделяем строку на две части по последнему пробелу
        grouped_assets[key] = value.replace("%",'')

    print(grouped_assets)
    percent_values = [float(value[:-1]) for value in grouped_assets.values()]

    # Посчитать сумму
    total = sum(percent_values)

    print(total)
    # breakpoint()

    return one_year, grouped_assets,AMC,OCF, date
    # return asset_values, date


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(one_year, assets, AMC, OCF, spreadsheet, filename, date):

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
                cellc.value = float(one_year)/100
                cellc.number_format = '0.00%'

                celld = sheet.range('D'+str(i+1))
                celld.value = float(AMC)/100
                celld.number_format = '0.00%'

                celle = sheet.range('E'+str(i+1))
                celle.value = float(OCF)/100
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
# 
    pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            one_year, assets, AMC, OCF, date = get_data(pdf)
            write_to_sheet(one_year, assets, AMC, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

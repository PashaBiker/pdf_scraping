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
from fuzzywuzzy import fuzz

excel_file = 'OCM Asset Management.xlsm'
pdf_folder = 'OCM PDFs'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path=r'E:\git\Scraping\OCM\poppler-23.07.0\Library\bin'


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

def ocr_from_pdf(pdf_path):
    # Конвертируем PDF в набор изображений
    images = convert_from_path(pdf_path, poppler_path=poppler_path, first_page=1, last_page=1)
    
    all_text = ""

    custom_config = r'--oem 3 --psm 6'

    for i, image in enumerate(images):
        # Если это первая страница, обрабатываем только её нижнюю левую часть
        if i == 0:
            # Вычисляем половину высоты и половину ширины изображения
            mid_height = int(image.height * 0.5)
            mid_width = int(image.width * 0.5)

            # Обрезаем изображение с середины до конца по высоте и с начала до середины по ширине
            cropped_image = image.crop((0, mid_height, mid_width, image.height))

            # Применяем Tesseract к обрезанному изображению
            picture_text = pytesseract.image_to_string(cropped_image, config=custom_config, lang='eng')
            all_text += picture_text + '\n'
        else:
            # Применяем Tesseract ко всему изображению для остальных страниц
            text = pytesseract.image_to_string(image, config=custom_config, lang='eng')
            all_text += text + '\n'
        
    return all_text

def get_data(file):

    date = ''

    try:
        with pdfplumber.open(file) as pdf:
            first_line_found = False
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                # print(text)
                
            
                for i, line in enumerate(text):

                    if "Ongoing Strategy Charge" in line:
                        for j in range(i+1, len(text)):
                            match = re.search(r'(\d+\.\d+)%', text[j])
                            if match:
                                OCF = match.group(1)
                                date = text[1]  
                                # print(OCF)
                                break

                    def extract_numbers(line):
                        elements = line.split()  # Разбиваем строку по пробелам

                        numbers = []
                        for elem in elements:
                            # Если элемент является числом
                            if re.match(r'[-+]?\d+\.\d+', elem.replace('%', '')):  # Удаление символа '%' перед проверкой
                                numbers.append(float(elem.replace('%', '')))
                            # Если элемент является прочерком
                            elif elem == "-":
                                numbers.append(0.0)
                        
                        return numbers

                    # Далее в вашем коде
                    numbers = extract_numbers(line)
                    if len(numbers) >= 3 and not first_line_found:
                        print(line)
                        one_month = numbers[0]
                        one_year = numbers[3] if len(numbers) > 3 else None  # Инициализация one_year
                        first_line_found = True
                        
                # print(date)
                # print(OCF)
                print(one_month)
                print(one_year)

                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Money Market',
                    'UK Fixed Interest',
                    'Global Fixed Interest',
                    'UK Gilts',
                    'Other Non-Equity',
                    'Property',
                    'Commodity & Energy',
                    'UK Equity',
                    'North American Equity',
                    'European Equity',
                    'Asian Equity',
                    'Other International Equity',
]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    with pdfplumber.open(file) as pdf:
        picture = ocr_from_pdf(file)
        picture_lines = picture.split('\n')
        start_index = next((i for i, s in enumerate(picture_lines) if "Asset Allocation" in s), None)

        if start_index is not None:
            filtered_data = picture_lines[start_index:]
        # print(filtered_data)
        # Initialize the asset_values dictionary with zeros
        asset_values = {word: 0 for word in asset_labels}

        corrections = {
            "aits": "gilts",
            "cits": "gilts",
            "aitts": "gilts",
            # добавьте другие известные коррекции здесь
        }

        for line in filtered_data:
            # Применить коррекции
            for wrong, correct in corrections.items():
                line = line.replace(wrong, correct)

            line_lower = line.lower()
            for word in asset_labels:
                if fuzz.partial_ratio(word.lower(), line_lower) > 80:
                    numbers = re.findall(r'\b(\d+\.?\d*)%', line)
                    if numbers:
                        number = float(numbers[-1])
                        asset_values[word] = number
                        break
        total = sum(asset_values.values())
        # print(asset_values)
        # print(total)
    return one_year,one_month, asset_values, OCF,date
    # return asset_values, date


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(one_year, one_month, assets, OCF, spreadsheet, filename, date):

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
                cellc.value = float(OCF)/100
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
            one_year,one_month, assets, OCF, date = get_data(pdf)
            # one_year , asset_values, date = get_data(pdf)
            write_to_sheet(one_year,one_month, assets, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)
            # write_to_sheet(one_year , asset_values, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

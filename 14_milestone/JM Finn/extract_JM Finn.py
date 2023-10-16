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
import io
excel_file = '14_milestone\JM Finn\JM Finn and Co.xlsm'
pdf_folder = '14_milestone\JM Finn\JM Finn PDFs'

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

    try:
        with pdfplumber.open(file) as pdf:
            first_line_found = False
            first_AMC_found = False
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                # print(text)

                for line in text:

                    if 'Investment Management' in line and not first_AMC_found:
                        AMC_number = re.findall(r'\d+\.?\d*', line)
                        AMC = AMC_number[0]
                        first_AMC_found = True
                        date_match = re.search(r'(\d{1,2})\w{2} (\w+) (\d{4})', text[1])
                        if date_match:
                            date = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}"

                    if 'Underlying Fund OCF' in line:
                        OCF_Number = re.findall(r'\d+\.?\d*', line)
                        OCF = OCF_Number[0]
                        # print(line)

                    numbers = re.findall(r'[-+]?\d+\.\d+%', line)
                    if len(numbers) >= 4 and not first_line_found:
                        one_year = numbers[2].replace('%','')  # Так как -1.5% это третье значение в списке numbers
                        first_line_found = True
                        
                # print(date)
                # print(AMC)
                # print(OCF)
                # print(one_year)

                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Cash',
                    'Fixed Income',
                    'Property & Real Assets',
                    'Absolute Return',
                    'UK Equity',
                    'US Equity',
                    'Europe ex-UK Equity',
                    'Japanese Equity',
                    'Global Emerging Market Equity',
                    'Global Developed Market Equity',]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Извлечение только левой половины страницы
            left_half = page.crop((0, 0, page.width / 2, page.height))
            text = left_half.extract_text()  # Извлекаем текст со страницы
        # print(page_text)
        
        # Разделяем текст на строки и добавляем их в список
        lines = text.split('\n')

        # Initialize the asset_values dictionary
        asset_values = {word: 0 for word in asset_labels}
        
        total = 0.0
        for line in lines:
            # Для каждой метки актива в asset_labels проверяем, содержится ли она в строке
            for label in asset_labels:
                if label in line:
                    # Если содержится, то используем регулярное выражение, чтобы извлечь числовое значение
                    value = re.search(r'(\d+\.\d+)', line.replace(label, ''))  # удаляем метку, чтобы избежать конфликтов
                    if value:
                        asset_values[label] = float(value.group(1))
                        asset_labels.remove(label)
                        total += float(value.group(1))

        print(asset_values)
        print(total)
 
    return one_year, asset_values,AMC,OCF, date
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
                cellc.value = float(AMC)/100
                cellc.number_format = '0,00%'

                celld = sheet.range('D'+str(i+1))
                celld.value = float(OCF)/100
                celld.number_format = '0,00%'

                celle = sheet.range('E'+str(i+1))
                celle.value = float(one_year)/100
                celle.number_format = '0,00%'

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
                    cell.number_format = '0,00%'


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

    pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            one_year, assets, AMC, OCF, date = get_data(pdf)
            write_to_sheet(one_year, assets, AMC, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

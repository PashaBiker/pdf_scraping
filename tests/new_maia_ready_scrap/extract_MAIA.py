import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
import time

excel_file = 'MAIA Asset Management.xlsm'
pdf_folder = 'MAIA PDFs'


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
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                # print(text)

                for i, line in enumerate(text):
                    if 'As at' in line:
                        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', line)
                        if date_match:
                            date_value = date_match.group(1)
                            modified_date = date_value.replace('/', '.')
                            date = modified_date

                    if 'Annual Management Charge' in line:
                        amc_ocf_line = text[i+1]
                        number = re.findall(r'\d+\.?\d*', amc_ocf_line)
                        AMC = number[0]
                        OCF = number[1]
                        
                print(date)
                print(AMC)
                print(OCF)

                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Fixed Interest',
                    'UK Equity',
                    'US Equity',
                    'European Equity',
                    'Japanese Equity',
                    'Asian Equity',
                    'Emerging Market Equity',
                    'Thematic Equity',
                    'Global Equity',
                    'Long Short Equity',
                    'Defined Returns',
                    'Gold',
                    'Infrastructure',
                    'Cash',]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    
    with pdfplumber.open(file) as pdf:
        text = ''

        # extract text from all pages
        for page in pdf.pages:
            # Get half of the width
            half_width = page.width / 2
            
            # Crop to the left half
            cropped_page = page.crop((0, 0, half_width, page.height))

            # Extract text from the cropped area
            text += cropped_page.extract_text()

        # Split the extracted text into lines
        lines = text.split('\n')
        # print(lines)
        # Initialize the asset_values dictionary
        asset_values = {word: 0 for word in asset_labels}
        
        start_processing = False
        end_processing = False
        total = 0
        for line in lines:
            if 'Asset Allocation' in line:
                start_processing = True

            if 'MAIA Risk Rating' in line:
                end_processing = True
                break  # Остановите цикл после того, как вы достигните конца обрабатываемого раздела

            if start_processing:
                for word in asset_labels:
                    if word in line:
                        # Извлекаем числа из строки
                        numbers = re.findall(r'\b(\d+)\b', line)  # Используем правильное регулярное выражение
                        if numbers:
                            number = int(numbers[-1])  # Преобразуем строку в число
                            asset_values[word] = number
                            total += float(number)

        # print(total)
        print(asset_values)
    return asset_values,AMC,OCF, date
    # return asset_values, date


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(assets, AMC, OCF, spreadsheet, filename, date):

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
                celld.value = float(OCF)/100
                celld.number_format = '0.00%'

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

    pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            assets, AMC, OCF, date = get_data(pdf)
            # one_year , asset_values, date = get_data(pdf)
            write_to_sheet(assets, AMC, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)
            # write_to_sheet(one_year , asset_values, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

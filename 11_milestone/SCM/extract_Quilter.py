import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
import time

excel_file = 'SCM Private.xlsm'
pdf_folder = 'SCM PDFs'


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
            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                # print(text)
                one_month = None
                one_year = None
                for line in text:
                    
                    if 'As at' in line:
                        date_match = re.search(r'(\d{1,2}\w{2}\s\w+\s\d{4})', text)
                        if date_match:
                            date = date_match.group(1).replace('th', '')  # Удаляем 'th'


                    if 'Annual Management Charge' in line:
                        AMC_number = re.findall(r'\d+\.?\d*', line)
                        AMC = AMC_number[0]
                        date = text[2]

                    if 'Weighted Cost of Underlying' in line:
                        OCF_Number = re.findall(r'\d+\.?\d*', line)
                        OCF = OCF_Number[0]
                        # print(line)

                    numbers = re.findall(r'[-+]?\d+\.\d+', line)
                    if len(numbers) >= 4 and not first_line_found:
                        numbers = re.findall(r'[-+]?\d+\.\d+', line)
                        # Get the first number
                        one_year = numbers[1]
                        first_line_found = True
                        
                # print(date)
                # print(AMC)
                # print(OCF)
                # print(one_year)
                # print(one_month)

                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['North American Equities',
                    'UK Equities',
                    'Fixed Interest',
                    'Alternatives',
                    'Global Equities',
                    "Cont'l European Equities",
                    'Cash Products',]

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    with pdfplumber.open(file) as pdf:
        text = ''
        
        # extract text from all pages
        for page in pdf.pages:
            text += page.extract_text()

        # Split the extracted text into lines
        lines = text.split('\n')
        print(lines)
        # Initialize the asset_values dictionary
        asset_values = {word: 0 for word in asset_labels}
        
        start_processing = False
        end_processing = False
        # total = 0
        for line in lines:
            if 'STRATEGY ASSET ALLOCATION' in line:
                start_processing = True

            if 'STRATEGY PERFORMANCE' in line:
                end_processing = True
                break  # Остановите цикл после того, как вы достигните конца обрабатываемого раздела

            if start_processing and not end_processing:
                for word in asset_labels:
                    if word in line:
                        numbers = re.findall(r'\b(\d+\.?\d*)%', line)
                        if numbers:
                            number = numbers[-1]
                            asset_values[word] = number
                            # total += float(number)

        # print(total)
        # print(asset_values)
    return one_year , asset_values,AMC,OCF, date
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

    # pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            one_year, assets, AMC, OCF, date = get_data(pdf)
            # one_year , asset_values, date = get_data(pdf)
            # write_to_sheet(one_year, assets, AMC, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)
            # write_to_sheet(one_year , asset_values, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

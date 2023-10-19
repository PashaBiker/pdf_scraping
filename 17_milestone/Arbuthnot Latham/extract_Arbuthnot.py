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

excel_file = 'Arbuthnot Latham.xlsm'
pdf_folder = 'Arbuthnot Latham PDFs'

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
        # print(link)
        # Get the corresponding filename from column A
        filename = sheet.range(f'A{row}').value + '.pdf'
        # print(filename)
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
    one_year = None
    two_years = None
    three_years = None
    four_years = None
    five_years = None
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                # Extract text from full page
                full_text = page.extract_text()
                lines = full_text.split('\n')

                # Extract date
                for line in lines:
                    if 'Portfolio Date' in line:
                        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', line)
                        if date_match:
                            extracted_date = date_match.group(1)
                            date = extracted_date.replace("/", ".")

                # Crop and extract text from the left half
                half_width = page.width / 2
                
                # Crop the left half of the page
                left_half = page.crop((0, 0, half_width, page.height))
                
                # Extract text from the cropped region
                text = left_half.extract_text()
                text = text.split('\n')
                # print(text)
                pattern = re.compile(r'\d{2}/\d{2}/\d{4} - \d{2}/\d{2}/\d{4} (-?\d+\.\d+)%')

                percentages = []
                for line in text:
                    match = pattern.search(line)
                    if match:
                        percentages.append(match.group(1))

                # Reverse the list to start from the most recent year
                percentages.reverse()

                # Assign values conditionally
                try:
                    one_year = percentages[0] 
                except IndexError:
                    one_year = None

                try:
                    two_years = percentages[1] 
                except IndexError:
                    two_years = None

                try:
                    three_years = percentages[2]
                except IndexError:
                    three_years = None

                try:
                    four_years = percentages[3]
                except IndexError:
                    four_years = None

                try:
                    five_years = percentages[4]
                except IndexError:
                    five_years = None

                break

        print(date)
        print(one_year)
        print(two_years)
        print(three_years)
        print(four_years)
        print(five_years)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Global Equity',	
                    'Other Fixed Interest',	
                    'Government Securities',	
                    'Property',	
                    'Absolute Return & Hedge Funds',	
                    'Other',	
                    'Cash',]   

    asset_labels = sorted(asset_labels, key=lambda x: len(x), reverse=True)

    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        
        # Устанавливаем границы обрезки по горизонтали
        # Crop and extract text from the left half
        half_width = page.width / 2
        
        # Crop the left half of the page
        left_half = page.crop((0, 0, half_width, page.height))
        text = left_half.extract_text()
        # Извлекаем текст с этой части страницы
        lines = text.split('\n')
        # print(lines)
        # Initialize the asset_values dictionary
        # asset_values = {word: 0 for word in asset_labels}
        lines = [re.sub(r'(\d) \.', r'\1.', line) for line in lines]

        # Initialize the asset_values dictionary
        asset_values = {}

        total = 0.0
        for line in lines:
            for label in asset_labels:
                if label in line:
                    modified_line = line.replace(label, '')  # удаляем метку, чтобы избежать конфликтов
                    value = re.search(r'(\d+\.\d+)', modified_line)
                    if value:
                        asset_values[label] = float(value.group(1))
                        asset_labels.remove(label)  # Удаляем метку, чтобы она больше не обрабатывалась
                        total += float(value.group(1))
                        break  # Выходим из внутреннего цикла, т.к. уже нашли значение

        print(asset_values)
        print(total)
        print('\n'*2)
 
    return one_year,two_years,three_years,four_years,five_years, asset_values, date
    # return asset_values, date


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(one_year,two_years,three_years,four_years,five_years, assets, spreadsheet, filename, date):

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
                if one_year is not None:
                    cellc.value = float(one_year)/100
                    cellc.number_format = '0.00%'
                
                celld = sheet.range('D'+str(i+1))
                if two_years is not None:
                    celld.value = float(two_years)/100
                    celld.number_format = '0.00%'
                
                celle = sheet.range('E'+str(i+1))
                if three_years is not None:
                    celle.value = float(three_years)/100
                    celle.number_format = '0.00%'
                
                cellf = sheet.range('F'+str(i+1))
                if four_years is not None:
                    cellf.value = float(four_years)/100
                    cellf.number_format = '0.00%'
                
                cellg = sheet.range('G'+str(i+1))
                if five_years is not None:
                    cellg.value = float(five_years)/100
                    cellg.number_format = '0.00%'


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
            one_year,two_years,three_years,four_years,five_years, assets, date = get_data(pdf)
            write_to_sheet(one_year,two_years,three_years,four_years,five_years, assets, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

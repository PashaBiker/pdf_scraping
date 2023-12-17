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
# import PyPDF2
import pdfplumber
import io
import PyPDF3
from pdfminer.high_level import extract_text

excel_file = '17_milestone\HSBC Asset Management\HSBC Asset Management.xlsm'
pdf_folder = '17_milestone\HSBC Asset Management\HSBC Asset Management PDFs'

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

def extract_left_text_from_page(page):
        # Calculate the x-coordinate which is 55% of the page width
        x_split = page.width * 0.54

        # Define the bounding box for the left 55%
        left_bbox = (0, 0, x_split, page.height)
        
        # Crop the page to the left 55% and extract text
        cropped_page = page.within_bbox(left_bbox)
        return cropped_page.extract_text()

def get_assets(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            asset_text = extract_left_text_from_page(pdf.pages[1])
            # print(asset_text.split('\n'))

        asset_labels = ['AsiaPac ex Japan Equity',
                        'Developed Equities (GBP hedged)',
                        'Liquidity',
                        'UK Equity',
                        'Japan Equity',
                        'Property',
                        'Global Equities',
                        'Europe ex UK Equity',
                        'Emerging Equity',
                        'Investment Grade Corporate Bonds (Global)',
                        'Global Government Bonds',
                        'US Equity',]  
        assets_result = {}
        # Convert the asset labels into a single regex pattern
        asset_labels_pattern = "|".join(map(re.escape, asset_labels))

        assets_result = {}
        for line in asset_text.split('\n'):
            match = re.search(asset_labels_pattern, line)
            if match:
                category = match.group(0)
                value_match = re.search(r'\b\d+(\.\d+)?', line[match.end():])
                if value_match:
                    value = value_match.group(0)
                    assets_result[category] = value

        print(assets_result)
        return assets_result

def get_data(pdf):
    extracted_text_1_page = extract_text(pdf, maxpages=1)
    text = extracted_text_1_page.split('\n')
    for i,line in enumerate(text):
        if 'Ongoing charge figure' in line:
            OCF = text[i+1].replace('%', '')
            print(OCF)

    with pdfplumber.open(pdf) as pdf:
        text = pdf.pages[1].extract_text()
        text = text.split('\n')
            
        for i, line in enumerate(text):
            if "6 month" in line:
                years_string = text[i+1]
                values = re.findall(r'-?\d+\.\d+', years_string)
                one_month = values[1]
                one_year = values[4]
                three_years = values[5]
                five_years = values[6]
                data_string = text[1]
                split_parts = re.split(r'(\d{2} \w+ \d{4})', data_string)
                date = split_parts[1]
                print(date)
                print(f"One Month: {one_month}")
                print(f"One Year: {one_year}")
                print(f"Three Years: {three_years}")
                print(f"Five Years: {five_years}")
    return OCF, one_month,one_year,three_years,five_years, date


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(OCF, one_month,one_year,three_years,five_years, assets, spreadsheet, filename, date):

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
                if OCF is not None:
                    cellc.value = float(OCF)/100
                    cellc.number_format = '0,00%'
                
                celld = sheet.range('D'+str(i+1))
                if one_month is not None:
                    celld.value = float(one_month)/100
                    celld.number_format = '0,00%'
                
                celle = sheet.range('E'+str(i+1))
                if one_year is not None:
                    celle.value = float(one_year)/100
                    celle.number_format = '0,00%'
                
                cellf = sheet.range('F'+str(i+1))
                if three_years is not None:
                    cellf.value = float(three_years)/100
                    cellf.number_format = '0,00%'
                
                cellg = sheet.range('G'+str(i+1))
                if five_years is not None:
                    cellg.value = float(five_years)/100
                    cellg.number_format = '0,00%'


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
            assets = get_assets(pdf)
            OCF, one_month,one_year,three_years,five_years, date = get_data(pdf)
            write_to_sheet(OCF, one_month,one_year,three_years,five_years, assets, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

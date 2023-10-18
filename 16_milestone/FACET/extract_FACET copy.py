import os
import traceback
import PyPDF2
import numpy as np
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
import easyocr
import fitz
from PIL import Image
from io import BytesIO


excel_file = '16_milestone\FACET\FACET.xlsm'
pdf_folder = '16_milestone\FACET\FACET PDFs'
output_image_folder="16_milestone\FACET\Cropped images"

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


def clean_date(data):
    match = re.search(r'(\d+)(st|nd|rd|th|tst) (\w+ \d+)', data)
    if match:
        day = match.group(1)
        month_year = match.group(3)
        return f"{day} {month_year}"
    return None


def get_data(file):

    date = ''

    try:
        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:
                text = page.extract_text()
                text = text.split('\n')
                # print(text)
                for line in text:
                    if 'except where indicated' in line:
                        print(line)
                        date = clean_date(line)

                    if 'Annual Management Charge' in line:
                        AMC_number = re.findall(r'(\d+\.\d+)%', line)
                        AMC = AMC_number[0]

                    if 'OCF ' in line:
                        OCF_Number = re.findall(r'\d+\.?\d*', line)
                        OCF = OCF_Number[0]
                                          
                print(date)
                print(AMC)
                print(OCF)
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

 
    return AMC,OCF, date
    # return asset_values, date


def is_within_range(resolution, target, px_range=10):
    width_check = target[0] - px_range <= resolution[0] <= target[0] + px_range
    height_check = target[1] - px_range <= resolution[1] <= target[1] + px_range
    return width_check and height_check

def pdf_image_extract(pdf_path, output_folder, pdf_name, page_num=None):
    allowed_resolutions = [(1018, 669), (1018, 556)]

    # Check if the output directory exists, if not create one
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_name = pdf_name.split('\\')[-1].replace('.pdf','')
    doc = fitz.open(pdf_path)
    extracted_images = []

    pages_to_process = [doc.load_page(page_num-1)] if page_num else [doc.load_page(i) for i in range(doc.page_count)]

    for page in pages_to_process:
        img_list = page.get_images(full=True)
        
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert image bytes to PIL Image for resolution check
            img_pil = Image.open(BytesIO(image_bytes))
            resolution = img_pil.size

            # Check if the resolution matches one of the allowed resolutions
            if any(is_within_range(resolution, allowed_res) for allowed_res in allowed_resolutions):
                # Construct the image path
                image_name = f"page_{page.number + 1}_img_{img_index + 1}_{pdf_name}.png"
                image_path = os.path.join(output_folder, image_name)

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                extracted_images.append(img_pil)

    print(f"Extracted images with the allowed resolutions are saved in {output_folder}")
    return extracted_images

def get_assets(pdf_path):
    extracted = pdf_image_extract(pdf_path=pdf_path, output_folder="16_milestone\FACET\Cropped images", pdf_name="assets_image", page_num=1)
    # TODO: CHANGE IMG TO PDF, 
    # Open the image using PIL
    img_pil = extracted[0]
    
    # Convert the PIL Image object to a numpy array
    img_np = np.array(img_pil)

    # Create the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    result = reader.readtext(img_np)

    keys = []

    # Extract only the percentages from the result
    for entry in result:
        text = entry[1].replace('/', '').replace(',', '.').replace('..', '.').replace('%', '').replace('|', '').strip()
        # print(text.split('\n'))

        # Extract all float numbers from the text
        numbers = re.findall(r"(\d+\.\d+|\d+)", text)

        # Add all valid numbers to keys
        for num in numbers:
            try:
                keys.append(float(num))
            except ValueError:
                pass

    # Create a dictionary by associating each asset with the respective percentage
    assets = ['Equities', 'Fixed Income', 'Property', 'Cash', 'Other']
    result_dict = {asset: keys[i*2] for i, asset in enumerate(assets)}

    # print(keys) # data from OCR
    # print(result_dict) # data from OCR + assets
    def truncate_number(num):
        s = str(num)
        if '.' in s:
            int_part, decimal_part = s.split('.')
            decimal_part = decimal_part[:2]  # Truncate without rounding
            return "{:.2f}".format(float(f"{int_part}.{decimal_part}"))
        return "{:.2f}".format(num)

    formatted_data = {k: truncate_number(v) for k, v in result_dict.items()}

    print(formatted_data) # output data
    return formatted_data

def crop_left_side(img, width=460):
    # No need to open the image again, just use the provided image
    
    # Crop 460px from the left
    left = 0
    upper = 0
    right = width
    lower = img.height
    cropped_img = img.crop((left, upper, right, lower))

    return cropped_img

def year_value(pdf_path):
    extracted = pdf_image_extract(pdf_path=pdf_path, output_folder=output_image_folder, pdf_name="years_image", page_num=2)
    # Open the image using PIL
    img_pil = extracted[0]
    
    cropped_img = crop_left_side(img_pil)
    
    # Convert the PIL Image object to a numpy array
    img_np = np.array(cropped_img)

    # Create the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)


    result = reader.readtext(img_np)

    keys = []

    # Extract only the percentages from the result
    for entry in result:
        text = entry[1]
        # print(text)
        keys.append(text.split('\n'))
    flattened_list = [item[0] for item in keys]
    print(flattened_list)
    digits_only = [item for item in flattened_list if re.match(r'^-?\d+(\.\d+)?$', item)]
    print(digits_only)

    one_month = None
    if len(digits_only) > 0 and digits_only[0]:
        one_month = digits_only[0]
    one_year = None
    if len(digits_only) > 3 and digits_only[3]:
        one_year = digits_only[3]

    three_years = None
    if len(digits_only) > 4 and digits_only[4]:
        three_years = digits_only[4]

    five_years = None
    if len(digits_only) > 5 and digits_only[5]:
        five_years = digits_only[5]
    print('one month ',one_month)
    print('one year ',one_year)
    print('three years ',three_years)
    print('five years ',five_years)

    return one_month, one_year, three_years, five_years

def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(one_month, one_year, three_years, five_years, assets, AMC, OCF, spreadsheet, filename, date):

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
                if AMC is not None:
                    cellc.value = float(AMC)/100
                    cellc.number_format = '0,00%'
                
                celld = sheet.range('D'+str(i+1))
                if OCF is not None:
                    celld.value = float(OCF)/100
                    celld.number_format = '0,00%'
                
                celle = sheet.range('E'+str(i+1))
                if one_month is not None:
                    celle.value = float(one_month)/100
                    celle.number_format = '0,00%'
                
                cellf = sheet.range('F'+str(i+1))
                if one_year is not None:
                    cellf.value = float(one_year)/100
                    cellf.number_format = '0,00%'
                
                cellg = sheet.range('G'+str(i+1))
                if three_years is not None:
                    cellg.value = float(three_years)/100
                    cellg.number_format = '0,00%'
                
                cellh = sheet.range('H'+str(i+1))
                if five_years is not None:
                    cellh.value = float(five_years)/100
                    cellh.number_format = '0,00%'

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
            AMC, OCF, date = get_data(pdf)
            one_month, one_year, three_years, five_years = year_value(pdf)
            assets = get_assets(pdf)
            write_to_sheet(one_month, one_year, three_years, five_years, assets, AMC, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

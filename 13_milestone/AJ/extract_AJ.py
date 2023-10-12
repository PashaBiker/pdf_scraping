import glob
import xlwings as xw
import requests
import os
import re
import traceback
import pdf2image
from PIL import Image
import pytesseract
import os

excel_file = 'AJ Bell.xlsm'
pdf_folder = 'AJ Bell PDFs'


poppler_path = r'poppler-23.07.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
directory = "pictures\\"

def get_data(file):
    print("[INFO] Converting PDF to images...")
    pages = pdf2image.convert_from_path(file,
                                        dpi=300, 
                                        first_page=2,
                                        poppler_path=poppler_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    page_image_paths = []
    for i, page in enumerate(pages, start=2):
        path = directory + f"page_{i}.png"
        page.save(path, 'PNG')
        page_image_paths.append(path)
        print(f"[INFO] Saved: {path}")

    print("[INFO] Extracting text from images using OCR...")
    page_texts = []
    def clean_text(lines, even_page):
        new_lines = []
        for line in lines:
            if even_page and '%' in line and 'OCF' not in line:
                line = re.sub(r'\b\d+(\.\d+)?%\b', '', line).strip()
            new_lines.append(line)
        return new_lines

    # Process each image path
    for index, path in enumerate(page_image_paths):
        print(f"[INFO] Processing image: {path}")
        text = pytesseract.image_to_string(Image.open(path))
        lines = [line.replace('J it','Japan equity').replace('Pacifi -','Pacific ex-').replace('UK equit','UK equity').replace('E -UK equit','Europe ex-UK equity') for line in text.split('\n') if line.strip() != '']
        # Check if page is even using its index
        even_page = (index + 1) % 2 == 0
        cleaned_lines = clean_text(lines, even_page)
        page_texts.append(cleaned_lines)

    data = page_texts

    print(data)

    Date = []

    for i, page in enumerate(data):
        if i % 2 == 0:
            for line in page[:7]:  # Check first 7 lines
                match = re.search(r'as at (.+)', line, re.IGNORECASE)
                if match:
                    date_str = match.group(1)
                    Date.append(date_str)

    print("[INFO] Extracting filename...")
    def remove_after_number(s):
        match = re.search(r"\d+", s)
        if match:
            return s[:match.end()]
        return s

    filename = [
    remove_after_number(page[1]) if re.search(r"\d+", page[1]) else 
    (remove_after_number(page[2]) if re.search(r"\d+", page[2]) else 
    remove_after_number(page[3]))
    for i, page in enumerate(data) if i % 2 == 0
    ]
    print("[INFO] Extracting OCF values...")
    OCF = []
    for page in data:
        for line in page:
            if "OCF" in line:
                percentage = line.split()[-1]
                if "%" in percentage:
                    OCF.append(float(percentage.replace('%',''))/100)
                    print('[INFO] OCF appended:', percentage)


    def clean_data(line):
        return re.sub(r"\d+\.\d+%", " ", line)

    cleaned_data = [[clean_data(line) for line in sublist] for sublist in data]

    print("[INFO] Extracting 1Y, 2Y, 3Y, 4Y, and 5Y values...")
    def insert_dot(match):
        year_set = {'2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'}
        matched_str = match.group()

        if matched_str not in year_set:
            return matched_str[:2] + '.' + matched_str[2:]
        return matched_str

    performance_values = []
    for i, page in enumerate(cleaned_data):
        if i % 2 != 0:
            # Modify lines to insert dots in four-digit sequences
            modified_page = [re.sub(r'\b(\d{4})\b', insert_dot, line) for line in page]
            
            # Find float values in the modified lines
            float_values = [re.findall(r"[-]?\d+\.\d+", line) for line in modified_page if len(re.findall(r"[-]?\d+\.\d+", line)) >= 2]
            print('[INFO] float_values =', float_values,)
            
            # Check if there are at least 3 lines with float values
            if len(float_values) >= 4:
                if len(float_values[2]) == 2 and len(float_values[3]) >= 3:
                    performance_values.append(float_values[3])
                    print('[INFO] Performance values appended:', float_values[3])
                else:
                    performance_values.append(float_values[2])
                    print('[INFO] Performance values appended:', float_values[2])
            elif len(float_values) == 3:
                performance_values.append(float_values[2])
                print('[INFO] Performance values appended:', float_values[2])
            elif len(float_values) == 2:
                performance_values.append(float_values[1])
                print('[INFO] Performance values appended (only 2 was):', float_values[1])
            else:
                print('[ERROR] Unexpected number of float values found in page.')

    print("[INFO] Extracting asset percentages...")
    asset_labels = [
        'UK equity',
        'North America equity',
        'Europe ex-UK equity',
        'Asia Pacific ex-Japan equity',
        'Japan equity',
        'Emerging Markets equity',
        'UK government bonds',
        'UK corporate bonds',
        'International bonds',
        'Property',
        'Cash equivalent',
        'Cash'
    ]
    
    asset_data = []

    for page in data:
        assets = {}
        for line in page:
            temp_line = line  # A temporary variable to store the line for further processing
            for label in sorted(asset_labels, key=lambda x: -len(x)):
                # Use findall to get all matches for the label in the line
                matches = re.findall(r"(\d+\.\d+)%\s*" + re.escape(label), temp_line)
                for match in matches:
                    value = match
                    assets[label] = float(value)  # Replace the value for that asset
                    # Remove the matched substring from temp_line
                    temp_line = temp_line.replace(f"{value}% {label}", '', 1)
        if assets:
            asset_data.append(assets)
            print('[INFO] Asset data appended for this page')   

    # print("[RESULTS] Filename:", filename)
    # print("[RESULTS] OCF:", OCF)
    # print("[RESULTS] Y values:", performance_values)
    # print("[RESULTS] Asset percentages:", asset_data)

    result2 = {}
    for i, name in enumerate(filename):  # assuming filename is a list of filenames
        Y1, Y2, Y3, Y4, Y5 = None, None, None, None, None

        year_values = performance_values[i]
        Y1 = float(year_values[0])/100 if len(year_values) > 0 else Y1
        Y2 = float(year_values[1])/100 if len(year_values) > 1 else Y2
        Y3 = float(year_values[2])/100 if len(year_values) > 2 else Y3
        Y4 = float(year_values[3])/100 if len(year_values) > 3 else Y4
        Y5 = float(year_values[4])/100 if len(year_values) > 4 else Y5    

        result2[name] = {
            'Date': Date[i],
            'Ongoing charges figure (OCF)': OCF[i],
            '1 Year': Y1,
            '2 Year': Y2,
            '3 Year': Y3,
            '4 Year': Y4,
            '5 Year': Y5,
            'Assets': asset_data[i]
        }
        print(
            'Date', Date[i],'\n',
            'Filename', name, "\n",
            'OCF', OCF[i], "\n",
            '1Y', Y1, "\n",
            '2Y', Y2, "\n",
            '3Y', Y3, "\n",
            '4Y', Y4, "\n",
            '5Y', Y5, "\n",
            'Assets', asset_data[i], "\n",
        )
    return result2


def download_pdfs(spreadsheet):
    print('Downloading PDFs...')
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets[1]

        # Create the folder if it doesn't exist
        folder_name = pdf_folder
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Start from row 3 and iterate through the links in column B
        last_row = sheet.range(
            'B' + str(sheet.cells.last_cell.row)).end('up').row
        for row in range(3, last_row+1):
            link = sheet.range(f'B{row}').value
            print(link)
            # Get the corresponding filename from column A
            filename = sheet.range(f'A{row}').value + '.pdf'

            try:
                # Download the PDF from the link
                headers = {
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
                if response.status_code == 200:
                    # If the filename is empty or None, use the last part of the link as the filename
                    if not filename:
                        filename = link.split('/')[-1]

                    # Save the PDF in the folder
                    file_path = os.path.join(folder_name, filename)

                    # Write the content of the downloaded PDF to the file
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    print(f"PDF downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading PDF {filename}: {str(e)}")

        wb.close()
        app.quit()

        print('All PDFs downloaded!')
        return folder_name

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def write_to_sheet(data, excel_file):

    try:
        app = xw.App(visible=False)
        wb = app.books.open(excel_file, update_links=False, read_only=False)

        for filename, values in data.items():
            print('Writing data of', filename)
            # Find the row that matches filename
            sheet = wb.sheets[2]

            row = None
            for cell in sheet.range('A:A'):
                if cell.value and cell.value.strip() == filename.strip():
                    row = cell.row
                    break

            if row is None:
                print(f"Filename '{filename}' not found in the sheet.")
                continue

            for key in values:
                if key == 'Assets':
                    continue

                # Find the matching column
                column = None
                for cell in sheet.range('1:1'):
                    if cell.value and cell.value.strip() == key.strip():
                        column = cell.column
                        break

                if column is None:
                    print(f"Column '{key}' not found in the sheet.")
                    continue

                # Write the key's value to the cell at the intersection of the row and column
                sheet.cells(row, column).value = values[key]

            sheet = wb.sheets[3]

            column_headings = sheet.range('A1').expand('right').value

            for asset, value in values['Assets'].items():
                if asset not in column_headings:
                    sheet.range(
                        f'{column_letter_from_index(len(column_headings)+1)}1').value = asset
                    # Update the column_headings list after adding the new column
                    column_headings = sheet.range('A1').expand('right').value

            for asset, value in values['Assets'].items():
                column_index = column_headings.index(asset) + 1
                cell = sheet.range(
                    f'{column_letter_from_index(column_index)}{row}')
                cell.value = float(value) / 100
                cell.number_format = '0.00%'

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

    pdf_folder = download_pdfs(excel_file)

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for file in pdfs:

        try:
            data = get_data(file)
            write_to_sheet(data, excel_file)

        except Exception as e:
            print(f"Error while processing {file}: {str(e)}")
            traceback.print_exc()

    print('\nDone!')

import os
import re
import PyPDF2
import cv2
import matplotlib.pyplot as plt
import numpy as np
import easyocr
import pdfplumber
from fuzzywuzzy import process
from pdf2image import convert_from_path
from PIL import Image
import glob
import xlwings as xw
import requests
import traceback


excel_file = 'Tideway Discretionary Fund Management Services.xlsm'
pdf_folder = 'Tideway pdfs'

# poppler path
poppler_path = r'C:\Program Files\poppler-23.07.0\Library\bin'

# output image path
output_image_path = "cropped_page.png"

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


def get_percentage_list(pdf_path):
    def main(color, image_path):

        image = cv2.imread(image_path)
        threshold = 40

        # Create mask for the given color
        lower_bound = np.array(color) - threshold
        upper_bound = np.array(color) + threshold
        mask = cv2.inRange(image, lower_bound, upper_bound)

        # Apply mask to the image
        result = cv2.bitwise_and(image, image, mask=mask)

        # Find contours in the mask
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('Cropped Image', result)
        # cv2.waitKey(0)

        MIN_CONTOUR_AREA = 500  # You can adjust this value
        output_data = []
        # Loop through the contours and crop the image based on bounding box of the contour
        for contour in contours:
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cropped_image = result[y:y+h, x:x+w]

            # Display cropped image
            # cv2.imshow('Cropped Image', cropped_image)
            # cv2.waitKey(0)

            gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            ocr_result = reader.readtext(cropped_image)

            extracted_text = ' '.join([item[1] for item in ocr_result])

            # Post-processing: Ensure only numbers remain
            # only_numbers = ''.join(filter(str.isdigit, extracted_text))
            output_text = extracted_text.replace(',', '').strip()
            # print(output_text)
            output_data.append(output_text)
            output_data = [item for item in output_data if item != '']
        cv2.destroyAllWindows()
        return output_data

    def extract_percentage_from_pdf(pdf_path):
        percentage_output = []

        with pdfplumber.open(pdf_path) as pdf:
            # Assuming you only want the second page's text
            page = pdf.pages[1]

            # Determine the new top boundary for cropping (50% of the page height)
            top_boundary = page.height * 0.5

            # Define the cropping box (bbox) as (x0, top, x1, bottom)
            cropped_page = page.crop(
                bbox=(0, top_boundary, page.width, page.height))

            # Extract text from the cropped area
            text = cropped_page.extract_text()
            # Split the text by spaces and check each word
            for word in text.split():
                if '%' in word:
                    # Clean the word and append to the list
                    cleaned_word = word.replace(
                        ',', '').replace(';', '').strip()
                    percentage_output.append(cleaned_word)

        return percentage_output
    
    def extract_text_from_pdf(pdf_path):
        text_output = []

        with pdfplumber.open(pdf_path) as pdf:
            # Assuming you only want the second page's text
            page = pdf.pages[1]

            # Determine the new top boundary for cropping (50% of the page height)
            top_boundary = page.height * 0.5

            # Define the cropping box (bbox) as (x0, top, x1, bottom)
            cropped_page = page.crop(
                bbox=(0, top_boundary, page.width, page.height))

            # Extract text from the cropped area
            text = cropped_page.extract_text()
            # Split the text by spaces and check each word
            text_output = text.split('\n')
            # text_output.append(text)

        return text_output

    def validation(data_text, output_data):
        THRESHOLD = 80

        # Create a list to hold the used matches
        used_matches = []

        # First process non-empty items in output_data
        for i, od in enumerate(output_data):
            if od:  # If the element is not empty
                # Exclude already used matches from the choices
                available_choices = [
                    dt for dt in data_text if dt not in used_matches]

                # Find its closest match among the available choices
                result = process.extractOne(od, available_choices)

                if result:  # Check if result is not None
                    closest_match, score = result

                    # Replace the current element with the closest match if it meets the threshold
                    if score >= THRESHOLD:
                        output_data[i] = closest_match
                        used_matches.append(closest_match)

        # Then fill empty items in output_data from data_text
        for i, od in enumerate(output_data):
            if not od:  # If the element is empty
                # Find a value from data_text that hasn't been used in output_data yet
                for dt in data_text:
                    if dt not in output_data and dt not in used_matches:
                        output_data[i] = dt
                        used_matches.append(dt)
                        break

        # Print and return the modified output_data
        return output_data
    
    def associate_labels_with_percentages(tags_found, percentages):
        assets_labels = [
            'Short-Dated Fixed Income (<5 years)',
            'Equity Growth',
            'Equity Income',
            'Alternatives',
            'Fixed Income (>5 years)'
        ]

        result_dict = {}

        for label in assets_labels:
            if label in tags_found:
                result_dict[label] = percentages[tags_found.index(label)]
            else:
                result_dict[label] = '0'

        return result_dict

    def image_pdf(pdf_path):
        pages = convert_from_path(
            pdf_path, dpi=300, poppler_path=poppler_path)
        second_page = pages[1]

        # Step 2: Crop the image based on given dimensions
        width, height = second_page.size
        left = 0
        right = int(0.62 * width)
        top = int(0.58 * height)
        bottom = int(0.88 * height)

        cropped_image = second_page.crop((left, top, right, bottom))

        # Step 3: Save the cropped image
        cropped_image.save(output_image_path)

        return output_image_path

    data = {'Dated_Fixed_Income': (193, 230, 231),
            'Equity_Growth': (88, 194, 173),
            'Equity_Income': (247, 148, 30),
            'Alternatives': (0, 174, 239),
            'Fixed_Income': (156, 203, 59)}
    
    assets_labels = ['Short-Dated',
                         'Equity Growth',
                         'Equity Income',
                         'Alternatives',
                         'Fixed Income', ]
    
    
    percentages = extract_percentage_from_pdf(pdf_path)
    pdf_text = extract_text_from_pdf(pdf_path)
    percentages.reverse()
    tags_found = []
    for text in pdf_text:
        for label in assets_labels:
            if label in text and label not in tags_found:
                tags_found.append(label)    
    print(tags_found, 'tags found')
    output = [label if label in tags_found else '' for label in assets_labels]
    tags_dict = dict(zip(tags_found, percentages))
    print(tags_dict, ' - tags_dict')
    print(percentages, '- extracted % from pdf')
    print(output, '- output names from pdf')
    output.reverse()
    print(output, '- reverse output names from pdf')
    # print(pdf_text, '- extracted text from pdf')
    output_data = []
    final_dict = associate_labels_with_percentages(tags_found, percentages)
    print(final_dict, '- final dict')
    image_path = image_pdf(pdf_path)

    for name, color in data.items():
        output_data.append(main(color, image_path))

    # print(output_data, '- extracted % with OCR from image_path')
    flattened_list = [item[0] if item else "" for item in output_data]
    flattened_list.reverse()
    # print(flattened_list, '- flattened_list')
    result = validation(percentages, flattened_list)
    result.reverse()
    print(result, '- validation list')
    non_empty_percentages = [p for p in result if p]

    # Reorder based on tags_found
    reordered_percentages = [non_empty_percentages.pop(0) if tag else '' for tag in output]

    print(reordered_percentages, "- output % from output")
    reordered_percentages.reverse()
    print(reordered_percentages, "- reverse output % from output")

    non_empty_count = sum(1 for p in reordered_percentages if p)

    if non_empty_count == 2 and 'Short-Dated' in tags_found:
        result = reordered_percentages[::-1]
        print(result,'we ret result from if   ')
    elif non_empty_count == 2:
        result = [tags_dict.get(label, '') for label in assets_labels]
        print(tags_dict, 'before result')
    elif non_empty_count > 2:
        result = reordered_percentages[::-1]


    result = [p for p in result if p != '0%']
    print(result, 'WE RETURN IT')
    return result


def get_data(file):

    with pdfplumber.open(file) as pdf:
        print(file)
        for page in pdf.pages:
            text = page.extract_text().split('\n')
            for i, line in enumerate(text):
                if 'as at' in line:
                    date = line.replace('th', '').split('as at ')[
                        1].strip().replace('.', '')

                if 'ongoing fund costs' in line:
                    OCF = re.findall(r'[-+]?\d+\.\d+', line)[0]

        print(date)
        print(OCF)

        assets_labels = ['Short-Dated Fixed Income (<5 years)',
                         'Equity Growth',
                         'Equity Income',
                         'Alternatives',
                         'Fixed Income (>5 years)', ]
        
        assets_percentage = get_percentage_list(file)
        print(assets_percentage)
        if assets_percentage == ['100%', '', '', '', '0%']:
            cleaned_percentage = [100, 0, 0, 0, 0]
        else:
            cleaned_percentage = [(p.replace('%', '')) for p in assets_percentage]

        # Zip the lists and convert to a dictionary
        asset_values = dict(zip(assets_labels, cleaned_percentage))

        print(asset_values)
    return asset_values, OCF, date


def write_to_sheet(assets, OCF, spreadsheet, filename, date):

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
                cellc.number_format = '0,00%'

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
                    cell = sheet.range(f'{column_letter_from_index(column_index)}{i+1}')
                    if value and str(value).replace(',', '').replace('.', '').isnumeric():
                        cell.value = float(str(value).replace(',', '')) / 100
                    else:
                        cell.value = None
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


if __name__ == "__main__":

    pdf_folder = download_pdfs(excel_file)  

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            assets, OCF, date = get_data(pdf)
            write_to_sheet(assets, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

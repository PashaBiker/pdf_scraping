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
import threading
from queue import Queue
from pdf2image import convert_from_path
import pytesseract
from pdfminer.high_level import extract_text

# YOUR PATH NEED TO BE ADDED
# YOUR PATH NEED TO BE ADDED
# YOUR PATH NEED TO BE ADDED
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path=r'D:\Git\pdf_scraping\11_milestone\Schroder\poppler-23.07.0\Library\bin'

excel_file = 'Schroder Investment Solutions.xlsm'
pdf_folder = 'Schroder PDFs'

def download_worker(q, folder_name):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
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

    while not q.empty():
        row_data = q.get()
        link, filename = row_data["link"], row_data["filename"]

        response = requests.get(link, headers=headers)
        if not filename:
            filename = link.split('/')[-1]

        file_path = os.path.join(folder_name, filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"PDF downloaded: {filename}")
        q.task_done()


def download_pdfs(spreadsheet):
    print('Downloading PDFs...')

    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets[1]

    folder_name = pdf_folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row

    q = Queue(maxsize=0)
    for row in range(3, last_row+1):
        link = sheet.range(f'B{row}').value
        filename = sheet.range(f'A{row}').value + '.pdf'
        q.put({"link": link, "filename": filename})

    num_threads = 4
    for _ in range(num_threads):
        worker_thread = threading.Thread(
            target=download_worker, args=(q, folder_name))
        worker_thread.start()

    q.join()

    wb.close()
    app.quit()

    print('All PDFs downloaded!')
    return folder_name


def get_data(file):

    date = ''
    AMC = None
    OCF = None
    try:
        with pdfplumber.open(file) as pdf:

            # data image OCR
            images = convert_from_path(file, poppler_path = poppler_path)
            first_page_image = images[0]
            cropped = first_page_image.crop((0, 0, first_page_image.width, first_page_image.height * 0.15))
            photo_text = pytesseract.image_to_string(cropped, lang="rus+eng")
            match = re.search(r'as at (\d{2}\.\d{2}\.\d{4})', photo_text)
            if match:
                date = match.group(1)

            # PDF Plumber for 1 month - 5 years
            first_page = pdf.pages[0]
            PDFPlumber_text = first_page.extract_text()
            PDFPlumber_text = PDFPlumber_text.split('\n')
            # print(PDFPlumber_text)

            # PyPDF2 reader for OCF AMC
            reader = PdfReader(file)
            page = reader.pages[0]
            PyPDF2_text = page.extract_text().split('\n')

            # PyPDF2 handler
            for line in PyPDF2_text:
                if 'Model portfolio fee' in line:
                    AMC_Number = re.findall(r'\d+\.?\d*', line)
                    if AMC_Number:
                        AMC = AMC_Number[0]
                
                if 'OCF' in line or 'Ongoing charge' in line:
                    OCF_Number = re.findall(r'\d+\.?\d*', line)
                    if OCF_Number:
                        OCF = OCF_Number[0]

            def extract_numbers(line):
                numbers = re.findall(r"(-?\d+\.\d+|-)", line)
                return [float(num) if num != '-' else None for num in numbers]
            
            # Поиск линии с "YTD" и "6 months"
            for i, line in enumerate(PDFPlumber_text):
                if "YTD" in line and "6 months" in line:
                    for next_line in PDFPlumber_text[i+1:]:
                        nums = extract_numbers(next_line)
                        if len(nums) > 3:
                            one_month = nums[0]
                            one_year = nums[4]
                            three_years = nums[5]
                            five_years = nums[6]
                            # print(nums[0], nums[4], nums[5], nums[6])
                            break
                    break

            # Поиск линии только с "YTD"
            for i, line in enumerate(PDFPlumber_text):
                if "YTD" in line and "6 months" not in line:
                    for next_line in PDFPlumber_text[i+1:]:
                        nums = extract_numbers(next_line)
                        if len(nums) > 3:
                            one_month = nums[0]
                            one_year = nums[3]
                            three_years = nums[4]
                            five_years = nums[5]
                            # print(nums[0], nums[3], nums[4], nums[5])
                            break

            print(date)
            print(AMC)
            print(OCF)
            print(one_month)
            print(one_year)
            print(three_years)
            print(five_years)

            # breakpoint()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    asset_labels = ['Bond',
                    'Cash',
                    'Stock',
                    'Other',
                    'Convertible',
                    'Preferred',
                    'Government bonds',
                    'Liquid Assets',
                    'Alternatives',
                    'Aggregate Bonds',
                    'Global Equity',
                    'UK Equity',
                    'Investment Grade Bonds',
                    'USA Equity',
                    'Property',
                    'Absolute Return',
                    'Emerging Market Debt Bonds',
                    'Europe Equity',
                    'Japan Equity',
                    'Emerging Market Equity',
                    'Other Equity',
                    'Global',
                    'Europe ex-UK/Middle East',
                    'Europe (excluding UK)',
                    'United Kingdom',
                    'Americas',
                    'Africa',
                    'Europe - Emerging',
                    'Japan',
                    'Pacific ex-Japan',
                    'Developed country',
                    'United States',
                    'Eurozone',
                    'Middle East',
                    'Europe - ex euro',
                    'Emerging Market',
                    'Asia - Developed',
                    'Asia - Emerging',
                    'Canada',
                    'Australasia',
                    'Latin America',
                    'Derivatives',
                    'Corporate',
                    'Government',
                    'Securitized',
                    'Technology',
                    'Financial services',
                    'Healthcare',
                    'Industrials',
                    'Consumer cyclical',
                    'Consumer defensive',
                    'Real estate',
                    'Communication Services',
                    'Cash & equivalents',
                    'Energy',
                    'Basic materials',
                    'Utilities',
                    'Hedge Funds',
                    'Asia Pacific ex Japan Equity',
                    'Commodities', ]

    asset_labels.sort(key=len, reverse=True)

    with pdfplumber.open(file) as pdf:
        left_text = ""
        right_text = ""

        for page in pdf.pages:
            # Разделяем страницу пополам по ширине
            half_width = page.width / 2

            # Извлекаем текст из левой половины страницы
            left_crop_box = (0, 0, half_width, page.height)
            left_cropped_page = page.crop(bbox=left_crop_box)
            left_text += left_cropped_page.extract_text() + "\n"

            # Извлекаем текст из правой половины страницы
            right_crop_box = (half_width, 0, page.width, page.height)
            right_cropped_page = page.crop(bbox=right_crop_box)
            right_text += right_cropped_page.extract_text() + "\n"

        combined_text = left_text + right_text
        data = combined_text.split('\n')
        # print(data)
        # print(lines.split('\n'))
        # Initialize the asset_values dictionary
        asset_values = {word: 0 for word in asset_labels}

        # Создаем словарь для хранения процентов каждого актива
        percentages = {}
        # Создаем словарь для отслеживания, сколько раз каждая метка актива была найдена
        sections = ["Asset class", "Sector", "Region", 'Top 10 holdings', 'Currency', 'Top 5 holdings']
        current_section = None

        percentages = {}

        for item in data:
            # Check for section names first
            for section in sections:
                if section in item:
                    current_section = section
                    break

            # Skip certain lines
            if not item.split() or (any(char.isdigit() for char in item.split()[0]) or "Portfolio" in item):
                continue

            # Your matching logic
            for label in asset_labels:
                cleaned_label = label.strip()
                match = re.search(
                    f'{re.escape(cleaned_label)} (\d+\.\d+)', item)
                if match:
                    cleaned_current_section = current_section.replace(
                        "  ", " ").strip()
                    key = f"{cleaned_current_section} {cleaned_label}"
                    percentages[key] = float(match.group(1))
                    break

    print(percentages)
    total_percentage = sum([value for key, value in percentages.items() if key != 'Top 10 holdings Other' and key != 'Currency'])
    print(total_percentage)

    return one_month, one_year, three_years, five_years, percentages, AMC, OCF, date
    # return asset_values, date


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
                cellb.value = date if date is not None else None

                cellc = sheet.range('C'+str(i+1))
                cellc.value = float(OCF)/100 if OCF is not None else None
                if cellc.value is not None:
                    cellc.number_format = '0.00%'

                celld = sheet.range('D'+str(i+1))
                celld.value = float(AMC)/100 if AMC is not None else None
                if celld.value is not None:
                    celld.number_format = '0.00%'

                celle = sheet.range('E'+str(i+1))
                celle.value = float(one_month)/100 if one_month is not None else None
                if celle.value is not None:
                    celle.number_format = '0.00%'

                cellf = sheet.range('F'+str(i+1))
                cellf.value = float(one_year)/100 if one_year is not None else None
                if cellf.value is not None:
                    cellf.number_format = '0.00%'

                cellg = sheet.range('G'+str(i+1))
                cellg.value = float(three_years)/100 if three_years is not None else None
                if cellg.value is not None:
                    cellg.number_format = '0.00%'

                cellh = sheet.range('H'+str(i+1))
                cellh.value = float(five_years)/100 if five_years is not None else None
                if cellh.value is not None:
                    cellh.number_format = '0.00%'

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
            print(pdf)
            one_month, one_year, three_years, five_years, assets, AMC, OCF, date = get_data(pdf)
            write_to_sheet(one_month, one_year, three_years, five_years, assets, AMC, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

        # print('Portfolio Cost:', portfolio_cost + '\t' + pdf)

    print('\nDone!')

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
import threading
from queue import Queue
import hashlib

excel_file = '17_milestone\Parmenion\Parmenion.xlsm'
pdf_folder = '17_milestone\Parmenion\Parmenion PDFs'


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


def get_data(pdf):
    with pdfplumber.open(pdf) as pdf:
        first_page_text = pdf.pages[0].extract_text()
        second_page_text = pdf.pages[1].extract_text()
        first_page_text = first_page_text.split('\n')
        second_page_text = second_page_text.split('\n')

        x0 = pdf.pages[0].width * 0.73
        cropped_page = pdf.pages[0].crop((x0, 0, pdf.pages[0].width, pdf.pages[0].height))
        cropped_first_page_text = cropped_page.extract_text().split('\n')
        print(first_page_text)

        # breakpoint()
        # print(second_page_text)
        founded_line = False
        for i, line in enumerate(cropped_first_page_text):
            if 'Underlying Funds OCF' in line:
                OCF = cropped_first_page_text[i+1].replace('%','')
                print(OCF)

            if 'DFM Charge' in line:
                charge = cropped_first_page_text[i+1].replace('%','')
                print(charge)

        for i, line in enumerate(first_page_text):
            if 'Cumulative Performance' in line:
                date_line = re.split(r'(?<=Cumulative Performance to )|(?= \(%\))', line)
                # print(date_line[1])
                date = date_line[1]

            if '6m' in line and not founded_line:
                year_line = first_page_text[i+1]
                # print(year_line)
                numbers = re.findall(r'-?\d+\.\d+', year_line)
                one_year = numbers[2]
                three_years = numbers[3]
                five_years = numbers[4]
                founded_line = True
                print(one_year)
                print(three_years)
                print(five_years)
                

        asset_labels = ['Managed Liquidity',
                        'Global Government Bonds',	
                        'Global Index-Linked Government Bonds',	
                        'Sterling Corporate Bonds',	
                        'Global Bonds',	
                        'Diversified Alternatives',	
                        'UK Equity Income',	
                        'UK Equity',	
                        'US Equity',	
                        'Europe ex UK Equity',
                        'Japan Equity',	
                        'Asia Pacific ex Japan Equity',	
                        'Emerging Markets Equity',	
                        'Managed Liquidity (Unscreened)',	
                        'UK Gilts',	
                        'International Equity',	
                        'Emerging Markets / Asia Pacific ex Japan Equity',]  
        assets_result = {}
        # Convert the asset labels into a single regex pattern
        # asset_labels_pattern = "|".join(map(re.escape, asset_labels))
        # asset_labels_pattern = sorted(asset_labels, key=lambda x: len(x), reverse=True)
        asset_labels_pattern = "|".join(map(re.escape, sorted(asset_labels, key=lambda x: len(x), reverse=True)))
        # Identify the start and end indices
        assets_result = {}

        start_index = -1
        end_index = -1

        # Identify the start and end indices
        for idx, line in enumerate(second_page_text):
            if 'Asset Allocation' in line:
                start_index = idx
            if 'Fund Allocation' in line:
                end_index = idx

        if start_index != -1 and end_index != -1:
            i = start_index + 1
            while i < end_index:
                line = second_page_text[i]
                match = re.search(asset_labels_pattern, line)
                if match:
                    category = match.group(0)
                    value_match = re.search(r'\b\d+(\.\d+)?%', line[match.end():])
                    if value_match:
                        value = value_match.group(0)[:-1]  # Remove the '%' sign
                        assets_result[category] = value
                        i += 1
                    else:
                        # If no value on this line, assume it's on the next line and combine them
                        if i + 1 < len(second_page_text):
                            line += second_page_text[i + 1]
                            value_match = re.search(r'\b\d+(\.\d+)?%', line[match.end():])
                            if value_match:
                                value = value_match.group(0)[:-1]  # Remove the '%' sign
                                assets_result[category] = value
                            i += 2
                else:
                    i += 1

        print(assets_result)
    return date, OCF, charge, one_year, three_years, five_years, assets_result


def clean_text(text):

    cleaned_line = re.sub(r'\d+\.?\d*', '', text)

    # Remove all spaces from the line and the word being searched
    cleaned_text = ''.join(cleaned_line.split())
    return cleaned_text


def write_to_sheet(OCF, charge, one_year, three_years, five_years, assets, spreadsheet, filename, date):

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
                if charge is not None:
                    celld.value = float(charge)/100
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

    # pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:
        try:
            date, OCF, charge, one_year, three_years, five_years, assets_result = get_data(pdf)
            write_to_sheet(OCF, charge, one_year, three_years, five_years, assets_result, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')

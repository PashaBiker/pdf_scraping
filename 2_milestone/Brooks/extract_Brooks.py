import glob
import pdfplumber
import xlwings as xw
import requests
import os
import re
import traceback

excel_file = 'Brooks Macdonald.xlsm'
pdf_folder = 'Brooks PDF'

def get_data(file):

    date = []
    Annual_management_charge = []
    OCF = []
    one_year = []

    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()

        text = text.split('\n')
        # print(text)

        for i, line in enumerate(text):
            if 'Annual management charge' in line:
                for offset in range(0, 3):  # check other lines
                    if i + offset < len(text):  # check if line is exist
                        founded_line = text[i+offset].strip()
                        if re.search(r'\d+\.\d+%', founded_line):  # if pattern found
                            perscent_pattern = r'\d+\.\d+%'
                            AMC = re.findall(perscent_pattern, founded_line)[0]
                            Annual_management_charge.append(AMC)
                            break  # if we found
                else:  # if breaked but line was not found
                    print("No one is seems like pattern.", line)
        # print(Annual_management_charge)

            if 'OCF ' in line:
                parts = line.split('%')  # split by '%'
                OCF.append(parts[0].strip().split()[1])  # take only first part and then add '%'

        # print(OCF)
            
            if '3M 6M 1Y 3Y 5Y' in line:
                for offset in range(1, 4):  # check other lines
                    if i + offset < len(text):  # check if line is exist
                        founded_line = text[i+offset].strip()
                        matches = re.findall(r'[+-]?\d+\.\d+', founded_line)
                        if len(matches) > 4:
                            cleaned_line = re.sub(r'.*?(MPS.*)', r'\1', founded_line)
                            numbers = re.findall(r'[+-]?\d+\.\d+', cleaned_line)
                            one_year.append(float(numbers[2])/100)
                            break  # if line founded

    text = ''

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    text = text.split('\n')
    text = [line for line in text if line.strip() != '']

    # print(text)

    filenames = []

    found_portfolio_holdings = False
    groups = []
    current_group = []

    for i, line in enumerate(text):
        if i == 0:
            filenames.append(text[1] + ' ' + text[2])
            date.append(text[3])
        elif i == len(text) - 1:
            continue
        else:
            if 'More information about the Brooks Macdonald Group can be found at www.brooksmacdonald.com' in line and i+3 < len(text):
                filenames.append(text[i+2] + " " + text[i+3])
                date.append(text[3])
            if 'Portfolio holdings' in line:
                found_portfolio_holdings = True
            elif 'Important information' in line:
                found_portfolio_holdings = False
                if current_group:
                    groups.append(current_group)
                    current_group = []
            elif found_portfolio_holdings:
                current_group.append(text[i].strip())

    print(filenames)

    categories = ["UK Fixed Interest", "International Fixed Interest", "UK Equities", "North American Equities",
        "European Equities", "Japan/Far East/Emerging","International & Thematic Equities", 
        "Hedge Funds & Alternatives", "Structured Return", "Cash"]

    categories_pattern = "|".join(categories)

    result = []

    for lst in groups:
        category_values = []
        # Сombine all in one string
        joined_string = " ".join(lst)
        # Ищем все вхождения категорий в объединенной строке
        for match in re.finditer(categories_pattern, joined_string):
            category = match.group(0)  # Получаем название категории
            # Получаем подстроку после найденной категории
            string_after_category = joined_string[match.end():]
            # Ищем первое число в подстроке (значение категории)
            value_match = re.search(r'\b\d+(\.\d+)?', string_after_category)
            if value_match:
                value = value_match.group(0)  # Получаем значение
                # Добавляем категорию и значение в список
                category_values.append(f"{category} {value}%")
        result.append(category_values)
    for i in range(len(result)):
        result[i] = list(dict.fromkeys(result[i]))
    # print(result)
    grouped_assets = []
    for group in result:
        keys = []
        values = []
        for line in group:
            key, value = line.rsplit(' ', 1)  # Разделяем строку на две части по последнему пробелу
            keys.append(key)
            values.append(value)
        assets = dict(zip(keys, values))
        grouped_assets.append(assets)

    result = {}

    for i, filename in enumerate(filenames):
        result[filename] = {
            'Date': date[i],
            '1 Year Performance': one_year[i],
            'Annual management charge (AMC)': Annual_management_charge[i],
            'OCF': OCF[i],
            'Assets': grouped_assets[i]
        }
        print(
            'Date', date[i], "\n",
            '12 months', one_year[i],"\n",
            'Estimated underlying fund charges', Annual_management_charge[i],"\n",
            'Management Fee', OCF[i],"\n",
            'Assets', grouped_assets[i],"\n",
            )
    
    return result


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
        last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row
        for row in range(3, last_row+1):
            link = sheet.range(f'B{row}').value
            print(link)
            # Get the corresponding filename from column A
            filename = sheet.range(f'A{row}').value + '.pdf'

            try:
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
                cell.value = float(value.replace('%', '')) / 100
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

    # enter the name of the excel file

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

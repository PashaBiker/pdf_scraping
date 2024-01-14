import glob
import pdfplumber
import xlwings as xw
import requests
import os
import traceback
from PyPDF2 import PdfReader
import re
import threading
from queue import Queue

excel_file = "abrdn.xlsm"

pdf_folder = "Abrdn pdfs"


def download_worker(q, folder_name):
    headers = {
        'authority': 'www.abrdn.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'abrdnjssintermediary#lang=en-GB; _gcl_au=1.1.1162956206.1702147479; _cs_c=1; ELOQUA=GUID=EDD2C907A9F947C8A383ECEC6CE4DDEB; OptanonAlertBoxClosed=2023-12-09T19:10:39.305Z; ORA_FPC=id=890b5499-d305-4770-bfcb-4fc600bd3d38; WTPERSIST=; abrdn-disclaimer=%5B%7B%22n%22%3A%22abrdnJssIntermediary%22%2C%22e%22%3A1709925040582%2C%22l%22%3A%22en-GB%22%7D%5D; bluekai_uid_plugin=ora.odc_dmp_bk_uuid,ceaAns9u999D94oA,ora.odc_dmp_bk_uuid_noslash,ceaAns9u999D94oA,ora.odc_source,bluekai; _ga=GA1.2.836657474.1702147479; _ga_TML7E2DDE5=GS1.1.1702491342.6.0.1702491343.59.0.0; _cs_id=2965f5a3-54fc-a02b-9ead-48dff31fec3f.1702147479.6.1702491343.1702491343.1.1736311479468; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Dec+13+2023+20%3A15%3A43+GMT%2B0200+(%D0%92%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4affb4e3-b240-488f-ad4e-af02837cf9ba&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=UA%3B68&AwaitingReconsent=false; ASP.NET_SessionId=nyjcyk0ilvoq1ojocom4j242',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
    asset_values = {}

    with pdfplumber.open(file) as pdf:
        tables = pdf.pages[1].extract_tables()
        for table in tables:
            for row in table:
                asset_values[row[0]] = row[1]

    reader = PdfReader(file)
    text = ""

    # extract text from all pages
    for page in reader.pages:
        text += page.extract_text()

    text = text.split("\n")

    data = {
        "Inception date": None,
        "Yield1": None,
        "Annual management fee": None,
        "Underlying OCF": None,
        "Date": None,
    }

    yield_pattern = re.compile(r"Yield[*1]")
    filename = file.split("\\")[-1].split(".")[0].split("-")[1]

    value_pattern = re.compile(r'\b-?\d+\.\d+\b|N/A')

    perf_labels = []
    perf_values = []
    found_labels = False

    for line in text:
        print(line)
        for key in data:
            if line.strip().startswith(key):
                data[key] = line.split(key)[1].strip()

        if (
            line.strip().startswith("Annual")
            and line.strip().endswith("%")
            and "fee" in line
        ):
            data["Annual management fee"] = line.split("fee")[1].strip()
            # print(line.split('fee')[1].strip())

        if line.strip().startswith("Underlying OCF"):
            data["Underlying OCF"] = line.split()[-1].strip()

        if line.strip().startswith("Underlying ongoing"):
            data["Underlying OCF"] = (
                text[text.index(line) + 1].split("figure")[-1].strip()
            )

        if yield_pattern.match(line.strip()):
            data["Yield1"] = line.split(yield_pattern.match(line.strip()).group())[
                1
            ].strip()

        if line.strip().startswith("1M 3M"):
            perf_labels = line.split()
            found_labels = True
        elif found_labels:
            # Look for d.dd patterns or "N/A" in the line
            line = re.sub(r'MPS \d', '', line)
            # Look for d.dd, -d.dd patterns or "N/A" in the line
            matches = value_pattern.findall(line)
            if matches:
                perf_values.extend(matches)
                # Reset flag as values are found
                found_labels = False
            
        if line.endswith(filename.strip()):
            # print(filename.strip(), "-файлнейм")
            # print("30 " + text[text.index(line) + 1].strip())
            data["Date"] = "30 " + text[text.index(line) + 1].strip()
            

    for label in perf_labels:
        if label == "Since":
            perf_labels[perf_labels.index(label)] = "Since Inception"

    perf_labels.append("Volatility2")
    print(perf_labels , 'perf_labels')
    print(perf_values , 'perf_values')
    performance = dict(zip(perf_labels, perf_values))

    print(data)
    print(performance)
    # print(asset_values)
    # print(f"Date: {date}")

    return data, performance, asset_values

def write_to_sheet(data, performances, assets, filename, excel_file):
    print(f"Writing data of: {filename}")

    try:
        app = xw.App(visible=False)
        wb = app.books.open(excel_file, update_links=False, read_only=False)
        sheet = wb.sheets[2]

        # Find the row that matches filename
        row = next(cell.row for cell in sheet.range("A:A") if cell.value == filename)

        # For every key in the data
        for key in data:
            # Find the matching column
            column = next(
                cell.column for cell in sheet.range("1:1") if cell.value == key
            )

            # Write the key's value to the cell at the intersection of the row and column
            sheet.cells(row, column).value = data[key]

            if "date" not in key.strip().lower():
                if data[key] is not None:
                    # Убедитесь, что data[key] не является None перед использованием .replace()
                    value = float(data[key].replace("%", "").replace(",", "")) / 100
                    sheet.cells(row, column).value = value
                    sheet.cells(row, column).number_format = "0.00%"
                else:
                    sheet.cells(row, column).value = None

        column_headings = sheet.range("A1").expand("right").value

        for key in performances:
            if key not in column_headings:
                # Find the first empty column dynamically
                empty_column_index = len(column_headings) + 1
                empty_column = column_letter_from_index(empty_column_index)

                # Assign the asset value to the first empty column
                cell = sheet.range(f"{empty_column}1")
                cell.value = key

                # Append the asset to column_headings
                column_headings.append(key)

        for key in performances:
            column_index = column_headings.index(key) + 1
            cell = sheet.range(f"{column_letter_from_index(column_index)}{row}")
            if performances[key] == "-" or performances[key] == "N/A":
                cell.value = ""  # or some default value
            else:
                cell.value = (
                    float(performances[key].replace(",", "").replace("%", "")) / 100
                )
            cell.number_format = "0.00%"

        sheet = wb.sheets[3]

        column_headings = sheet.range("A1").expand("right").value

        for asset in assets:
            if asset not in column_headings:
                # Find the first empty column dynamically
                empty_column_index = len(column_headings) + 1
                empty_column = column_letter_from_index(empty_column_index)

                # Assign the asset value to the first empty column
                cell = sheet.range(f"{empty_column}1")
                cell.value = asset

                # Append the asset to column_headings
                column_headings.append(asset)

        range_values = sheet.range("A1").expand().value

        for i in range(len(range_values)):
            if filename in range_values[i]:
                for asset, value in assets.items():
                    column_index = column_headings.index(asset) + 1
                    cell = sheet.range(f"{column_letter_from_index(column_index)}{i+1}")
                    cell.value = float(value.replace(",", "").replace("%", "")) / 100
                    cell.number_format = "0.00%"

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


if __name__ == "__main__":

    pdf_folder = download_pdfs(excel_file)

    pdfs = glob.glob(pdf_folder + "/*.pdf")

    for file in pdfs:
        try:
            print()
            data, performance, assets = get_data(file)
            filename = file.split("\\")[-1].split(".")[0]
            write_to_sheet(data, performance, assets, filename, excel_file)

        except Exception as e:
            print(f"Error while processing {file}: {str(e)}")
            traceback.print_exc()

    print("\nDone!")

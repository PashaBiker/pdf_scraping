import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
from pdfminer.high_level import extract_text
import fitz


def download_pdfs(spreadsheet):
    print("Downloading PDFs...")
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets[1]

        # Create the folder if it doesn't exist
        folder_name = "Tideway pdfs"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Start from row 3 and iterate through the links in column B
        for row in range(3, sheet.range("B3").end("down").row + 1):
            link = sheet.range(f"B{row}").value
            # Get the corresponding filename from column A
            filename = sheet.range(f"A{row}").value + ".pdf"

            try:
                # Download the PDF from the link
                response = requests.get(link)
                if response.status_code == 200:
                    # If the filename is empty or None, use the last part of the link as the filename
                    if not filename:
                        filename = link.split("/")[-1]

                    # Save the PDF in the folder
                    file_path = os.path.join(folder_name, filename)

                    # Write the content of the downloaded PDF to the file
                    with open(file_path, "wb") as f:
                        f.write(response.content)

                    print(f"PDF downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading PDF {filename}: {str(e)}")

        wb.close()
        app.quit()

        print("All PDFs downloaded!")
        return folder_name

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_data(file):
    filename = file.split("\\")[-1].split(".")[0]
    print(f"Extracting data of: {filename}")

    text = ""

    perf_time = []
    perf_val = []

    asset_name = []
    asset_val = []

    ocf = ""
    date = ""
    # try:
    doc = fitz.open(file)
    for page in doc:
        text += page.get_text()

    text = text.split("\n")

    is_asset = True

    for i, line in enumerate(reversed(text), 1):
        if line.strip() and line[0].isalpha() and is_asset == False:
            break
        if line.strip() and line[0].isalpha() and is_asset == True:
            asset_name.append(line.strip())
            continue

        if line.strip() and line[-1] == "%":
            asset_val.append(line.strip())
            is_asset = False
            continue

    is_perf = False

    text = extract_text(file)
    text = text.split("\n")

    for line in text:
        if line.startswith("Cumulative Performance (%)"):
            is_perf = True
            continue
        if line.startswith("IA") and is_perf == True:
            is_perf = False
            break
        if is_perf:
            if line.strip():
                if line[-1].isalpha():
                    perf_time.append(line.strip())
                elif line[-1] == "%":
                    perf_val.append(line.strip())


    new_asset_val = []

    for i in asset_val:
        parts = i.split("%")
        if len(parts) > 1:
            reversed_parts = parts[::-1]  # Reversing the parts
            new_asset_val.extend(reversed_parts)
        else:
            new_asset_val.append(parts[0].strip())

    asset_val = [asset for asset in new_asset_val if asset]


    assets = dict(zip(asset_name, asset_val))

    data = {
        "Date": date,
        "Ongoing Charges Figure (OCF)": ocf,
    }

    return data, assets, filename


def replace_keys(assets: dict) -> dict:
    old_keys = [
        "European Equities",
        "Emerging Markets Equities",
        "Global Equities",
    ]
    new_keys = ["European Equity", "Emerging Market Equity", "Global Equity"]
    for old_key, new_key in zip(old_keys, new_keys):
        if old_key in assets:
            assets[new_key] = assets.pop(old_key)
    return assets


def write_to_sheet(data, assets, filename, excel_file):
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
                cell.column
                for cell in sheet.range("1:1")
                if cell.value != None and cell.value.strip() == key.strip()
            )
            # Write the key's value to the cell at the intersection of the row and column
            sheet.cells(row, column).value = data[key]

            if key != "Date" and data[key] != "":
                sheet.cells(row, column).value = (
                    float(data[key].replace(",", "").replace("%", "")) / 100
                )
                sheet.cells(row, column).number_format = "0.00%"

            if key == "Date":
                sheet.cells(row, column).number_format = "dd/mm/yyyy"

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
    # enter the name of the excel file
    excel_file = "Tideway Discretionary Fund Management Services.xlsm"

    # pdf_folder = download_pdfs(excel_file)
    pdf_folder = "Tideway pdfs"

    pdfs = glob.glob(pdf_folder + "/*.pdf")

    # get_data(pdfs[6])

    for pdf in pdfs:
        try:
            # get_data(pdf)
            print("--------------------")
            data, assets, filename = get_data(pdf)
            assets = replace_keys(assets)
            write_to_sheet(data, assets, filename, excel_file)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")
            traceback.print_exc()

    print("\nDone!")

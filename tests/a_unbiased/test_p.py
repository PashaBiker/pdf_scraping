import openpyxl
import pandas as pd

def extract_column_data(file_name, column_letter, sheet_name=None):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook[sheet_name] if sheet_name else workbook.active
    data = [cell.value for cell in sheet[column_letter] if cell.value is not None]
    workbook.close()
    return data

file_name = "tests/unbiased/UK postcodes.xlsx"
column_letter = "A"
postcodes = extract_column_data(file_name, column_letter)

for postcode in postcodes:
    print(postcode)
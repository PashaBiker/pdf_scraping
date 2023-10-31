import openpyxl

def extract_column_data(file_name, column_letter, sheet_name=None):
    
    # Load the Excel workbook and select the desired sheet
    workbook = openpyxl.load_workbook(file_name)
    if sheet_name:
        sheet = workbook[sheet_name]
    else:
        sheet = workbook.active  # default to the first sheet
    
    # Get the column data
    data = [cell.value for cell in sheet[column_letter] if cell.value is not None]
    
    workbook.close()
    return data

# Input details
file_name = "tests/find_adviser/UK postcodes.xlsx"  # Replace with the path to your Excel file
column_letter = "A"  # Replace with the desired column letter

# Extract and print data
column_data = extract_column_data(file_name, column_letter)
for cell_value in column_data:
    print(cell_value)


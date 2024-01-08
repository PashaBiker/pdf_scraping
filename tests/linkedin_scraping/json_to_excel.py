import json
import pandas as pd

def json_to_excel(json_data, excel_file_name):
    # Convert JSON data to pandas DataFrame
    df = pd.DataFrame(json_data)

    # Write DataFrame to Excel file
    df.to_excel(excel_file_name, index=False)

# Example usage
file_path = 'updated_data_with_linkedin.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    json_data = json.load(file)


json_to_excel(json_data, 'output.xlsx')

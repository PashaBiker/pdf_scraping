import pandas as pd
import json

def excel_to_json(excel_file, json_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Convert the DataFrame to a JSON string
    json_str = df.to_json(orient='records', indent=4)

    # Write the JSON string to a file
    with open(json_file, 'w') as f:
        f.write(json_str)

# Example usage
excel_to_json('namelink_titles_worksfors.xlsx', 'tests/linkedin_scraping/namelink_titles_worksfors.json')

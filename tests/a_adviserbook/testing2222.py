import json
import pandas as pd

# Load JSON data
filename = 'tests/a_adviserbook/managers_output.json' # Replace with your actual JSON file path
with open(filename, 'r') as file:
    json_data = json.load(file)

# Initialize empty list for advisers data
advisers_data = []

# Process JSON data
for key, value in json_data.items():
    firm_info = value['firm']
    
    # Assume the first office is the main office
    main_office = firm_info.get('offices', [{}])[0]

    # Advisers data
    for adviser_item in value.get('advisers_fca', []):
        if isinstance(adviser_item, str):
            try:
                adviser = json.loads(adviser_item)  # Parse string to dictionary
            except json.JSONDecodeError:
                print(f"Failed to parse adviser data: {adviser_item}")
                continue
        elif isinstance(adviser_item, dict):
            adviser = adviser_item
        else:
            print(f"Unexpected data type in advisers_fca: {type(adviser_item)}")
            continue

        advisers_data.append({
            'title': adviser.get('salutation', ''),
            'firstname': adviser.get('firstname', ''),
            'surname': adviser.get('surname', ''),
            'fca_num': adviser.get('fca_num', ''),
            'company_name': firm_info.get('name', ''),
            'website': firm_info.get('website', ''),
            'company_email': firm_info.get('email', ''),
            'company_linkedin': firm_info.get('linkedin', ''),
            'address_line2': main_office.get('address_line2', ''),
            'office_phone_number': main_office.get('phone_number', ''),
            'postcode': main_office.get('postcode', '')
        })

# Create a DataFrame
df_advisers = pd.DataFrame(advisers_data)

# Define the desired column order
desired_order = [
    'title', 'firstname', 'surname', 'fca_num', 'company_name', 'website', 'company_email', 
    'company_linkedin', 'address_line2', 'office_phone_number', 'postcode'
]

# Reorder DataFrame columns according to the desired order
df_advisers = df_advisers[desired_order]

# Save to Excel
excel_path = 'new_advisers_fca.xlsx'
df_advisers.to_excel(excel_path, sheet_name='Advisers FCA', index=False)

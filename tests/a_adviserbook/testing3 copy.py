import json
import pandas as pd

# Load JSON data
filename = 'tests/a_adviserbook/managers_output.json' # Replace with your actual JSON file path
with open(filename, 'r') as file:
    json_data = json.load(file)

# Initialize empty lists for each category of data
firms_data = []
advisers_data = []

# Process JSON data
for key, value in json_data.items():
    firm_info = value['firm']
    
    # Assume the first office is the main office
    main_office = firm_info.get('offices', [{}])[0]

    # Advisers data
    for adviser in firm_info.get('advisers_fca', []):
        advisers_data.append({
            'title': adviser.get('title', ''),
            'salutation': adviser.get('salutation', ''),
            'firstname': adviser.get('firstname', ''),
            'surname': adviser.get('surname', ''),
            'phone_number': adviser.get('phone_number', ''),
            'email': adviser.get('email', ''),
            'linkedin': adviser.get('linkedin', ''),
            'fca_num': firm_info.get('fca_num', ''),
            'company_name': firm_info.get('name', ''),
            'alternative_name': firm_info.get('alternative_name', ''),
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
    'title','salutation', 'firstname', 'surname', 'phone_number', 'email', 'linkedin', 
    'fca_num', 'company_name', 'alternative_name', 'website', 'company_email', 'company_linkedin', 
    'address_line2', 'office_phone_number', 'postcode'
]

# Reorder DataFrame columns according to the desired order
df_advisers = df_advisers[desired_order]

# Rename columns to avoid duplication and match the desired output
df_advisers.rename(columns={
    'company_email': 'email', 
    'company_linkedin': 'linkedin',
    'office_phone_number': 'phone_number'
}, inplace=True)

# Save to Excel
excel_path = 'advisers_fca.xlsx'
df_advisers.to_excel(excel_path, sheet_name='Advisers FCA', index=False)

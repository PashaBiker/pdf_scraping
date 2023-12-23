import json
import pandas as pd

filename = 'tests/a_adviserbook/managers_output.json'

with open(filename, 'r') as file:
    json_data = json.load(file)

firms_data = []
advisers_data = []
offices_data = []
advisers_fca_data = []
advisers_fca_strings = []  # List to store string items from advisers_fca

for key, value in json_data.items():
    # Firm data
    firm_info = value['firm']
    firms_data.append({
        'fca_num': firm_info.get('fca_num', ''),
        'name': firm_info.get('name', ''),
        'alternative_name': firm_info.get('alternative_name', ''),
        'website': firm_info.get('website', ''),
        'email': firm_info.get('email', ''),
        'linkedin': firm_info.get('linkedin', '')
    })

    # Advisers data
    for adviser in firm_info.get('advisers', []):
        advisers_data.append({
            'title': adviser.get('title', ''),
            'firstname': adviser.get('firstname', ''),
            'surname': adviser.get('surname', ''),
            'phone_number': adviser.get('phone_number', ''),
            'email': adviser.get('email', ''),
            'linkedin': adviser.get('linkedin', '')
        })

    # Offices data
    for office in firm_info.get('offices', []):
        offices_data.append({
            'address_line2': office.get('address_line2', ''),
            'phone_number': office.get('phone_number', ''),
            'postcode': office.get('postcode', '')
        })

    # Advisers FCA data
    for adviser_fca in value.get('advisers_fca', []):
        if isinstance(adviser_fca, dict):
            advisers_fca_data.append({
                'salutation': adviser_fca.get('salutation', ''),
                'firstname': adviser_fca.get('firstname', ''),
                'surname': adviser_fca.get('surname', ''),
                'phone_number': adviser_fca.get('phone_number', ''),
                'email': adviser_fca.get('email', ''),
                'linkedin': adviser_fca.get('linkedin', '')
            })
        elif isinstance(adviser_fca, str):
            advisers_fca_strings.append(adviser_fca)

# Creating DataFrames
df_firms = pd.DataFrame(firms_data)
df_advisers = pd.DataFrame(advisers_data)
df_offices = pd.DataFrame(offices_data)
df_advisers_fca = pd.DataFrame(advisers_fca_data)
df_advisers_fca_strings = pd.DataFrame({'IRN': advisers_fca_strings})  # DataFrame for the string items

# Creating an Excel writer object and writing DataFrames to Excel
excel_path = 'firms_data.xlsx'
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    df_firms.to_excel(writer, sheet_name='Firm', index=False)
    df_advisers.to_excel(writer, sheet_name='Advisers', index=False)
    df_offices.to_excel(writer, sheet_name='Offices', index=False)
    df_advisers_fca.to_excel(writer, sheet_name='Advisers_FCA', index=False)
    df_advisers_fca_strings.to_excel(writer, sheet_name='Advisers_FCA_Strings', index=False)

# Rest of your code...

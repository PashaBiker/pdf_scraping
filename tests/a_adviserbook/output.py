import json

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        # print("Data loaded from file:", data)  # Diagnostic print
        return data

def remove_duplicates(companies):
    unique = {}
    for company in companies:
        fca_num = company.get('fca_num')
        if fca_num and fca_num not in unique:
            unique[fca_num] = company
    return list(unique.values())

def save_to_file(companies, filename):
    with open(filename, 'w') as file:
        json.dump(companies, file, indent=4)

# File containing the JSON data
input_filename = 'tests/a_adviserbook/unique_filtered_companies.json'
output_filename = 'tests/a_adviserbook/unique_filtered_companies_emails.json'

# Read, filter, remove duplicates, and save
data = read_json_file(input_filename)
# unique_companies = remove_duplicates(data)
# save_to_file(unique_companies, output_filename)

print(f"Filtered companies saved to {output_filename}")

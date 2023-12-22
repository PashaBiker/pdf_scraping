import json

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        # print("Data loaded from file:", data)  # Diagnostic print
        return data


def filter_companies(input_file, output_file):
    try:
        # Load the data from the input file
        with open(input_file, 'r') as file:
            data = json.load(file)

        # Filter companies based on the criteria
        filtered_companies = []
        for company in data:
            if not isinstance(company, dict):
                print(f"Skipping non-dict item: {company}")
                continue

            # Safely get 'specialities' and 'services' as lists
            specialities = company.get("specialities", [])
            if isinstance(specialities, str):
                specialities = [specialities]

            services = company.get("services", [])
            if isinstance(services, str):
                services = [services]

            # Check for 'investment' in specialities or 'investments' in services
            if "investment" in specialities or "investments" in services:
                filtered_companies.append(company)
            else:
                print(f"Skipping company (does not meet criteria): {company['firm_name']}")

        # Save the filtered data to the output file
        with open(output_file, 'w') as file:
            json.dump(filtered_companies, file, indent=4)

        if filtered_companies:
            print(f"Filtered companies saved to {output_file}")
        else:
            print("No companies matched the filtering criteria.")

    except Exception as e:
        print(f"An error occurred: {e}")

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
input_filename = 'tests/a_adviserbook/output.json'
output_filename = 'tests/a_adviserbook/filtered_companies.json'

# Read, filter, remove duplicates, and save
data = read_json_file(input_filename)
filter_companies(input_filename, output_filename)
# unique_companies = remove_duplicates(filtered_companies)
# save_to_file(filtered_companies, output_filename)

print(f"Filtered companies saved to {output_filename}")

import json
import re

file_path = '3k_postcodes_delete_name_surname_website.json'

# Reading the JSON file
with open(file_path, 'r') as file:
    records = json.load(file)
# Parse the JSON data

# Filter out persons who don't have a website
persons_no_website = [person for person in records if not person["website"]]

# Convert to JSON string
no_website_json = json.dumps(persons_no_website, indent=4)


for item in records:
    match = re.search(r'/([^/]+)-(\d+)$', item['url'])
    if match:
        company_name = match.group(1).replace('-', ' ')
        item["company_name"] = company_name

updated_json_data = json.dumps(records, indent=4)

# Save to a new JSON file
no_website_file_path = 'company_names_website.json'
with open(no_website_file_path, 'w') as file:
    file.write(updated_json_data)
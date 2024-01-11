



import json


file_path = 'tests/linkedin_scraping/namelink_titles_worksfors.json'






with open(file_path, 'r') as file:
    json_data = json.load(file)


for entry in json_data:
    entry["allname"] += " UK"

with open('uk_namelink_titles_worksfors.json', 'w') as file:
    x = json.dumps(json_data, indent=4)
    file.write(x)
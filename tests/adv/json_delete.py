import json

# Replace 'your_file.json' with your actual file path
file_path = '3k_postcodes_delete_name_surname_website.json'

# Reading the JSON file
with open(file_path, 'r') as file:
    records = json.load(file)
# Parse the JSON data

# Function to remove duplicates
def remove_duplicates(records):
    seen = set()
    unique_records = []
    for record in records:
        identifier = (record['name'], record['surname'], record['website'])
        if identifier not in seen:
            seen.add(identifier)
            unique_records.append(record)
    return unique_records

# Remove duplicates
# unique_records = remove_duplicates(records)

filtered_data = []
for item in records:
    filtered_data.append({
        "title": item["title"],
        "name": item["name"],
        "surname": item["surname"],
        "job": item["job"],
        "iovoxNumber": item["iovoxNumber"],
        "phone": item["phone"],
        "address": item["address"],
        "website": item["website"],
        "linkedin": item["linkedin"]
    })

# Convert to JSON string
# filtered_json = json.dumps(filtered_data, indent=4)

# Convert back to JSON
with open('filtered_data.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(filtered_data, indent=4))
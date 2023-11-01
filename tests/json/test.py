import json

data = [{
    "Manager's Name": "Mr Adam Fearn DipPFS",
    "Company's Name": "cakescyb",
    "Email": "adam@absolutef2s.co.uk",
    "Webpage": 'absolutefwebpages.co.uk',
    "Phone Number": "01664 562825",
    "Postcode": "LE13 0SW,"
}]

with open("tests/json/final_result.json", "r") as file:
    data = json.load(file)

def extract_domain(url):
    if url:
        parts = url.split('//')[-1].split('@')[-1].split('/')
        return parts[0]
    return None

def edit_json(item):
    webpage = item.get("Webpage")
    email = item.get("Email")

    # Extract domain from webpage
    domain = extract_domain(webpage)

    # If domain is None or webpage is not present, extract from email
    if not domain:
        domain = extract_domain(email)

    # Add the URL to the data
    if domain:
        item["URL"] = "www." + domain

    return item

# Edit the JSON data for each item in the list
edited_data = [edit_json(item) for item in data]

# Print the edited JSON
print(json.dumps(edited_data, indent=4))
with open('tests/json/urls_output_list_full.json', 'w') as file:
    json.dump(edited_data, file, indent=4)


















import json
# with open("tests/json/company_names3.json", "r") as file:
with open("tests/json/titles_list_full.json", "r") as file:
    json_data = json.load(file)

# for item in json_data:
#     if "Title" not in item:
#         item["Title"] = None
# List of titles that need to be cleared
titles_to_clear = [
    "No title",
    "No title found",
    "Home - ",
    "Home | ",
    "Homepage | ",
    "403 Forbidden",
    "Service unavailable",
    "Gmail",
    "404 Page no found",
    "Site Not Configured | 404 Not Found",
    "Untitled Document",
    "Homepage - ",
    "Web Server's Default Page",
    "Bot Verification",
    "Find a financial adviser near you | ",
    "Apache2 Ubuntu Default Page: It works",
    "404 - File or directory not found.",
    'Yahoo | Mail, Weather, Search, Politics, News, Finance, Sports & Videos',
    'AlmusWealth.com is for sale | HugeDomains',
    'Home - Financial advisers, investment, wealth management and pensions advice  - ',
    'Welcome to ',
    'Domain Default page',


]

# Update the JSON structure
for item in json_data:
    title = item["Title"]
    if title:
        for unwanted_title in titles_to_clear:
            if unwanted_title in title:
                item["Title"] = title.replace(unwanted_title, "").strip()
        if item["Title"] == "":
            item["Title"] = None

# Update the JSON structure
for item in json_data:
    if item["Title"] in titles_to_clear:
        item["Title"] = None
# Print the updated JSON
print(json.dumps(json_data, indent=4))

with open('tests/json/eedited_titles_list_full.json', 'w') as file:
    json.dump(json_data, file, indent=4)

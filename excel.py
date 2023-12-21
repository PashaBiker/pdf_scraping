import json
import pandas as pd

# Load JSON data
with open('company_names_website.json', 'r') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel('filtered_company_names.xlsx', index=False)
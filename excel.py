import json
import pandas as pd

# Load JSON data
with open('filtered_data.json', 'r') as file:
    data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel('filtered.xlsx', index=False)
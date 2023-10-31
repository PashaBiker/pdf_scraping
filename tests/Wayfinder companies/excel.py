








import json
import pandas as pd

filename = "tests/Wayfinder copy/final_output_list.json"

with open(filename, 'r') as file:
    data = json.load(file)


df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel("output_companies.xlsx", index=False)
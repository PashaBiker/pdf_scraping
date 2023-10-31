








import json
import pandas as pd

filename = "tests/Wayfinder/first_part.json"

with open(filename, 'r') as file:
    data = json.load(file)


df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel("output.xlsx", index=False)
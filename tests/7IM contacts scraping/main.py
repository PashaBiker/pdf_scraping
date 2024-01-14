
import re
from bs4 import BeautifulSoup
import pandas as pd

with open ('tests/7IM contacts scraping/7IM.html', 'r', encoding='UTF-8') as html:
    html_content = html.read()


# Function to parse HTML and extract table data
def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all("td")
        cols = [ele.text.strip().replace('\n', ' ').replace('\r', '') for ele in cols]
        data.append(cols)
    return data

# Extract data from HTML
data = extract_table_data(html_content)

# Create a DataFrame and save to Excel
column_headers = ["Discretionary Fund Manager", "Active Annual Management Fee", "ESG Annual Management Fee", "Contact Information"]
df = pd.DataFrame(data, columns=column_headers)
excel_file_path = 'tests/7IM contacts scraping/2extracted_table_data.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Data extracted and saved to {excel_file_path}")
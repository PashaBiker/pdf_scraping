

import re
from bs4 import BeautifulSoup
import pandas as pd

with open ('tests/abrdn_contacts/abrdn.html', 'r', encoding='UTF-8') as html:
    html = html.read()

# Function to parse HTML and extract data
def extract_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    for h4 in soup.find_all("h4"):
        company_name = h4.get_text().strip()
        p = h4.find_next_sibling("p")
        if p:
            contact_name = p.get_text().split('\n')[0].strip()
            phone = p.find('a', href=lambda href: href and "tel:" in href)
            email = p.find('a', href=lambda href: href and "mailto:" in href)
            website = p.find('a', href=lambda href: href and "http://" in href or "https://" in href)
            
            phone_number = phone.get_text().strip() if phone else ''
            email_address = email.get_text().strip() if email else ''
            website_url = website['href'].strip() if website else ''

            data.append([company_name, contact_name, phone_number, email_address, website_url])
    return data

# Extract data from HTML
data = extract_data(html)

# Create a DataFrame and save to Excel
df = pd.DataFrame(data, columns=["Company Name", "Contact Name", "Phone Number", "Email Address", "Website URL"])
excel_file_path = 'tests/new_scraping_sites/extracted_contact_info.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Data extracted and saved to {excel_file_path}")

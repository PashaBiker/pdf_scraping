



import re
from bs4 import BeautifulSoup
import pandas as pd

with open ('tests/fidelity_contacts/fidelty.html', 'r', encoding='UTF-8') as html:
    html = html.read()

# print(html)


html_content = '''
<dd>
<p><strong>Blackfinch Investments limited</strong><br>
<strong>Contact name:&nbsp;</strong>Alice Bollen<br>
<strong>Contact details: E:&nbsp;</strong><a href="mailto:enquiries@blackfinch.com" data-di-id="di-id-5fc8de4b-8268b084">enquiries@blackfinch.com</a>/&nbsp;<a href="mailto:a.bollen@blackfinch.com" data-di-id="di-id-c23c336d-75b4f1d7">a.bollen@blackfinch.com</a>&nbsp;<strong>T:</strong>&nbsp;01452 717 755<br>
<strong>Consumer Duty:&nbsp;</strong><a href="https://blackfinch.com/esg" target="_blank" data-di-id="di-id-a71f89f1-f8f32476">https://blackfinch.com/esg</a><br>
<strong>Date confirmed:</strong>&nbsp;24.07.23</p></dd>
'''
soup = BeautifulSoup(html, 'html.parser')
# soup = BeautifulSoup(html_content, 'html.parser')

data_list = []  # List to store each entry as a dictionary

dds = soup.findAll('dd')
for dd in dds:
    ps = dd.findAll('p')
    for p in ps:
        data_entry = {'Name': None, 'Contact Name': None, 'Emails': None, 'Telephone': None, 'MPhone': None}

        # Extracting the name
        name_tag = p.find('strong')
        data_entry['Name'] = name_tag.get_text() if name_tag else 'Not Found'

        # Extracting contact name, telephone, and mobile phone
        for strong_tag in p.find_all('strong'):
            if "Contact name:" in strong_tag.get_text():
                data_entry['Contact Name'] = strong_tag.next_sibling.strip() if strong_tag.next_sibling else 'Not Found'
            if "T:" in strong_tag.get_text():
                data_entry['Telephone'] = strong_tag.next_sibling.strip().replace(' or', '') if strong_tag.next_sibling else 'Not Found'
            if "M:" in strong_tag.get_text():
                data_entry['MPhone'] = strong_tag.next_sibling.strip() if strong_tag.next_sibling else 'Not Found'

        # Extracting emails
        contact_details_tag = p.find('strong', text=lambda text: text and 'Contact details: E:' in text)
        emails = []
        if contact_details_tag:
            for sibling in contact_details_tag.find_next_siblings():
                if sibling.name == 'a' and sibling.get('href', '').startswith('mailto:'):
                    emails.append(sibling.get_text())
        data_entry['Emails'] = ', '.join(emails) if emails else 'Not Found'

        data_list.append(data_entry)

# Convert to DataFrame
df = pd.DataFrame(data_list)

# Export to Excel
excel_file_path = "tests/new_scraping_sites/fidelity.xlsx"  # Change this to your desired file path
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data saved to {excel_file_path}")
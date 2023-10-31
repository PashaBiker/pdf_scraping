import json
from bs4 import BeautifulSoup
import requests


html_file_path = 'tests\Wayfinder\html.html'
with open(html_file_path, 'r') as file:
    # Read the content of the file and store it in the variable
    html = file.read()


soup = BeautifulSoup(html, 'html.parser')

# Find all divs with the class 'nonFPweekWrapper wayfinderProfile row'
divs = soup.find_all('div', class_='afpfWrapper nonFPweekWrapper')
output = []
for div in divs:
    manager_name = div.find('h3').text
    company_name = div.find('h4').text
    find_out_more_link = "https://www.cisi.org" + div.find('a', class_='btn btn-default findMoreLink')['href']
    
    # Extracting the 'Visit website' link. If not present, set to None.
    website_link_element = div.find('a', class_='btn btn-primary websiteLink')
    companys_webpage_link = website_link_element['href'] if website_link_element else None

    output.append({
        'manager_name': manager_name,
        'company_name': company_name,
        'find_out_more_link': find_out_more_link,
        'companys_webpage_link': companys_webpage_link
    })

print(json.dumps(output, indent=4))


for entry in data:
    response = requests.get(entry['find_out_more_link'])
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract postcode (from the last <br> tag of the wayfinderAddress div)
    address_div = soup.find('div', class_='wayfinderAddress')
    if address_div:
        entry['postcode'] = address_div.contents[-1].strip()

    # Extract phone number and email
    contact_div = soup.find('div', class_='wayfinderContactDetails')
    if contact_div:
        # Extracting phone number
        phone_element = contact_div.find('span', class_='fas fa-phone')
        if phone_element:
            entry['phone_number'] = phone_element.find_next_sibling(text=True).strip()

        # Extracting email
        email_element = contact_div.find('a', class_='profileEmail btn btn-primary webButton')
        if email_element and 'mailto:' in email_element['href']:
            entry['email'] = email_element['href'].replace('mailto:', '').strip()

print(json.dumps(data, indent=4))
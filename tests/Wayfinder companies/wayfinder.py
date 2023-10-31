import json
from bs4 import BeautifulSoup
import requests


html_file_path = 'tests\Wayfinder copy\html.html'
with open(html_file_path, 'r') as file:
    # Read the content of the file and store it in the variable
    html = file.read()


soup = BeautifulSoup(html, 'html.parser')

# Find all divs with the class 'nonFPweekWrapper wayfinderProfile row'
divs = soup.find_all('div', class_='afpfWrapper nonFPweekWrapper')
output = []
for div in divs:
    company_name = div.find('h3').text
    # manager_name = div.find('h3').text
    find_out_more_link = "https://www.cisi.org" + div.find('a', class_='btn btn-default findMoreLink')['href']
    
    # Extracting the 'Visit website' link. If not present, set to None.
    website_link_element = div.find('a', class_='btn btn-primary websiteLink')
    companys_webpage_link = website_link_element['href'] if website_link_element else None

    output.append({
        'company_name': company_name,
        'find_out_more_link': find_out_more_link,
        'companys_webpage_link': companys_webpage_link
    })

print(json.dumps(output, indent=4))
with open('output_list.json', 'w') as file:
    json.dump(output, file, indent=4)
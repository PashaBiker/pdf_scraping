from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

session = HTMLSession()

for item in data:
    url = item['find_out_more_link']
    driver = webdriver.Chrome()

    # Use the find_out_more_link to get the HTML
    url = data[0]["find_out_more_link"]
    driver.get(url)

    # Get the page's HTML source
    # breakpoint()
    wait = WebDriverWait(driver, 10)  # wait for 10 seconds
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wayfinderAddressBlock"]/div')))

    html_source = driver.page_source

    # You can print it to see the HTML content
    # print(html_source)
    soup = BeautifulSoup(html_source, 'html.parser')

    address_div = soup.find('div', class_='wayfinderAddress')

    if address_div:
        contents = address_div.contents
        company_name = contents[0].text if contents[0].name == 'b' else None

        # Create an address list based on the contents after the company name
        address_list = [str(item) for item in contents[1:] if isinstance(item, str) or item.name == 'br']

        # Extract postcode which is the string content after the last <br/>
        last_br_index = max(idx for idx, val in enumerate(address_list) if val == '<br/>')
        postcode = address_list[last_br_index + 1] if last_br_index < len(address_list) - 1 else None
        item['postcode'] = postcode
        # print(contents)

    # Extract email and phone number
    contact_div = soup.find('div', class_='wayfinderContactDetails')
    if contact_div:
        phone_p = contact_div.find('p')
        email_a = contact_div.find('a', class_='profileEmail')

        phone_number = phone_p.get_text(strip=True) if phone_p else None
        email = email_a['href'].replace('mailto:', '') if email_a else None

        item['phone_number'] = phone_number
        item['email'] = email

print(json.dumps(data, indent=4))
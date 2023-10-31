from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

filename = "tests\Wayfinder copy\output_comoanies_list.json"  # filename stored in a variable

# Read the data from a file
with open(filename, 'r') as file:
    data = json.load(file)

def process_item(item):
    url = item['find_out_more_link']
    driver = webdriver.Chrome()

    # Use the find_out_more_link to get the HTML
    driver.get(url)

    wait = WebDriverWait(driver, 10)  # wait for 10 seconds
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wayfinderAddressBlock"]/div')))

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    address_div = soup.find('div', class_='wayfinderAddress')
    if address_div:
        contents = address_div.contents
        company_name = contents[0].text if contents[0].name == 'b' else None
        address_list = [str(item) for item in contents[1:] if isinstance(item, str) or item.name == 'br']
        last_br_index = max(idx for idx, val in enumerate(address_list) if val == '<br/>')
        postcode = address_list[last_br_index + 1] if last_br_index < len(address_list) - 1 else None
        item['postcode'] = postcode

    # Extract email and phone number
    contact_div = soup.find('div', class_='wayfinderContactDetails')
    if contact_div:
        phone_p = contact_div.find('p')
        email_a = contact_div.find('a', class_='profileEmail')

        phone_number = phone_p.get_text(strip=True) if phone_p else None
        email = email_a['href'].replace('mailto:', '') if email_a else None

        item['phone_number'] = phone_number
        item['email'] = email

    driver.close()

# Maximum of 10 threads in the pool. You can adjust based on your system's capacity.
with ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(process_item, data)

print(json.dumps(data, indent=4))
with open('final_output_list.json', 'w') as file:
    json.dump(data, file, indent=4)

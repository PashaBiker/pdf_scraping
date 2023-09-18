from bs4 import BeautifulSoup
import xlwings as xw
import traceback
from bs4 import BeautifulSoup
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
fund_data= []
driver.get('https://www.schroders.com/en-gb/uk/intermediary/investment-solutions/fund-centre/#/fund/SCHDR_F00000YK97/schroder-tactical-portfolio-5-f-acc/GB00BZCR4F60/profile/')
# WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/div[12]/div/fx-document-group-panel/div/fx-documents-panel/div[2]/div/div[2]/div[2]/fx-document-item/div/a")))
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div/div[12]')))
# Находим все элементы div с указанным классом
time.sleep(3)

element = driver.find_element(By.CSS_SELECTOR, '.fundexplorer-documentitem')
driver.execute_script("arguments[0].scrollIntoView();", element)
link_elements = driver.find_elements(By.CSS_SELECTOR, '.historical-document-item')

for link in link_elements:
    # Check if 'Factsheet' is in the link text
    if 'Factsheet' in link.text:
        print(link.get_attribute('href'))
        
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

driver.quit()

div_tag_file_links_all = soup.findAll('div', {'class': 'col-block-items layout-layout3 fundexplorer-documentitem'})
for div_tag_file_links in div_tag_file_links_all:
    factsheet_element = div_tag_file_links.find('h2', text='Factsheet')
    # Извлекаем родительский элемент 'a' для этого заголовка и получаем значение href
    factsheet_href = factsheet_element.find_parent('a')['href']
    # factsheet_anchor = div_tag_file_links.find('a', {'data-test-id': 'fundDashboardPageDocumentItem', 'class': 'document-item'}, string="Factsheet", recursive=True)
    # factsheet_link = factsheet_anchor['href']
print(factsheet_href)


div_tag = soup.find('div', {'class': 'fund-info valign-middle'})
# Из этого div извлекаем текст из тега <strong> внутри <h1>
fund_name_div = div_tag.h1.strong.text

# Убираем " F Acc", если оно есть в тексте
fund_name_text = fund_name_div.replace(' F Acc', '')

fund_data[fund_name_text] = factsheet_href

print(fund_data)


breakpoint()
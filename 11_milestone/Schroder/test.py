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

url = 'https://www.schroders.com/en-gb/uk/intermediary/investment-solutions/fund-centre/#/fund/SCHDR_F000016OTO/schroder-active-portfolio-3/-/profile/'


fund_data = {}

driver = webdriver.Chrome()
driver.get(url)
# time.sleep(5)
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div/div[1]/div/div/div[12]/div/fx-document-group-panel/div/fx-documents-panel/div[2]/div/div[2]/div[2]/fx-document-item/div/a")))
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
div_tag = soup.find('div', {'class': 'fund-info valign-middle'})

# Из этого div извлекаем текст из тега <strong> внутри <h1>
fund_name_div = div_tag.h1.strong.text

# Убираем " F Acc", если оно есть в тексте
fund_name_text = fund_name_div.replace(' F Acc', '')
anchor = soup.findAll('a', {'data-test-id': 'fundDashboardPageDocumentItem'})
# for fund_name in anchor:
#     # fund_name_text = fund_name.h2.text
#     fact_sheet_link = fund_name['href']
#     fund_data[fund_name_text] = fact_sheet_link
for link in anchor:
    title = link.find('h2')
    if title and title.text.strip() == 'Factsheet':
        fact_sheet_link = link['href']
        fund_data[fund_name_text] = fact_sheet_link
print(fund_data)
driver.quit()
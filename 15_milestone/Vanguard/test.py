from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the driver
driver = webdriver.Chrome()

# Navigate to the price-performance URL
base_url = "https://www.vanguardinvestor.co.uk/investments/vanguard-lifestrategy-40-equity-fund-accumulation-shares/"
price_performance_url = base_url + "price-performance"
driver.get(price_performance_url)

# Wait until the specific element appears and click the button
element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/ukd-link-tabs/div/div/div/nav/button[6]'))
element = WebDriverWait(driver, 30).until(element_present)

button = driver.find_element(By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/ukd-link-tabs/div/div/div/nav/button[6]')
driver.execute_script("arguments[0].scrollIntoView();", button)
time.sleep(2)  # Дайте немного времени после скролла перед тем, как кликнуть
button.click()
# Extract and print the table content
table = driver.find_element(By.CLASS_NAME, 'responsive-scrollable-table')
table_text = table.text
text = table_text.split('\n')
print(text)

ocf = driver.find_element(By.XPATH,'//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/ukd-link-tabs/div/span')
ocf_text = ocf.text
print(ocf_text)

date = driver.find_element(By.XPATH,'//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-price-performance/ukd-past-performance/p[1]')
date_text = date.text
print(date_text)




# Navigate to the portfolio-data URL
portfolio_data_url = base_url + "portfolio-data"
driver.get(portfolio_data_url)

# Wait until the specific element appears
element_present_portfolio = EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-portfolio-data/ukd-underlying-allocations/div'))
element_portfolio = WebDriverWait(driver, 30).until(element_present_portfolio)

# Extract and print the table content
table_portfolio = driver.find_element(By.XPATH, '//*[@id="main-content"]/ukd-fund-detail/div[2]/ukd-portfolio-data/ukd-underlying-allocations/div/div/table')
print(table_portfolio.text.split('\n'))

# Close the driver
driver.quit()

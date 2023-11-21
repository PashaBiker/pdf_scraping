import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging
import platform

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Установка цикла событий для Windows
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

with open('data.json', 'r') as file:
    json_funds = json.load(file)
    logger.info("Файл JSON загружен.")

funds = json_funds[:5000]
logger.info(f"Обработка первых {len(funds)} фондов.")

headers = {
    'authority': 'tools.morningstar.co.uk',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://www.morningstar.co.uk',
    'referer': 'https://www.morningstar.co.uk/uk/screener/fund.aspx',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

async def get_domicile_and_inception_date(session, url, params, semaphore):
    timeout = aiohttp.ClientTimeout(total=20)  # 20 seconds timeout
    async with semaphore, session.get(url, params=params, headers=headers, timeout=timeout) as response:
        content = await response.text()
        soup = BeautifulSoup(content, 'html.parser')

        management_div = soup.find('div', id='managementManagementFundManagerDiv')
        if management_div:
            # Поиск таблицы внутри div
            table = management_div.find('table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable managementManagementTable')
            if table:
                rows = table.find_all('tr')

                domicile = 'Not found'
                inception_date = 'Not found'

                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) == 2:
                        label, value = cols[0].text.strip(), cols[1].text.strip()

                        if label == 'Domicile':
                            domicile = value
                        elif label == 'Inception Date':
                            inception_date = value


                logger.info(f"Domicile: {domicile}, Inception Date: {inception_date} для SecId: {params['id']}")
                return domicile, inception_date

        logger.warning(f"Данные не найдены для SecId: {params['id']}")
        return 'Domicile not found', 'Inception Date not found'

async def process_funds():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(20)  # Adjust the concurrency level as needed
        tasks = [asyncio.create_task(get_domicile_and_inception_date(session, 'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx', {'id': fund['SecId'], 'tab': '4'}, semaphore)) for fund in funds]
        results = await asyncio.gather(*tasks)

        for fund, (domicile, inception_date) in zip(funds, results):
            fund['Domicile'] = domicile
            fund['InceptionDate'] = inception_date

        logger.info("Funds processing completed.")

asyncio.run(process_funds())

# Сохранение обновленных данных в файл
with open('111111111111data_dom_date222222222222.json', 'w') as file:
    json.dump(funds, file)
    logger.info("Данные сохранены в файл data_dom_date.json.")
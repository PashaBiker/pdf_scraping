import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import logging


with open('data.json', 'r') as file:
    # Загрузка содержимого JSON файла в переменную
    json_funds = json.load(file)

funds = json_funds[:5000]

# Параметры для HTTP-запроса (примеры)

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

# Асинхронная функция для получения заголовка из HTML
async def get_domicile_and_inception_date(session, url, params):
    async with session.get(url, params=params, headers=headers) as response:
        content = await response.text()
        soup = BeautifulSoup(content, 'html.parser')

        # Поиск всех div с нужным классом
        management_divs = soup.find_all('div', class_='managementManagementFundManagerDiv')

        for div in management_divs:
            # В каждом div ищем таблицу
            table = div.find('table', class_='snapshotTextColor snapshotTextFontStyle snapshotTable managementManagementTable')
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

                return domicile, inception_date

        return 'Domicile not found', 'Inception Date not found'

# Асинхронная функция для обработки каждого фонда
async def process_funds():
    connector = aiohttp.TCPConnector(limit_per_host=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for fund in funds:
            params = {
                'id': fund['SecId'],
                'tab': '4',
            }
            task = asyncio.create_task(get_domicile_and_inception_date(session, 'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx', params))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # Добавление заголовков и дат основания в словари фондов
        for fund, (domicile, inception_date) in zip(funds, results):
            fund['Domicile'] = domicile
            fund['InceptionDate'] = inception_date

# Запуск асинхронной обработки
asyncio.run(process_funds())

# Вывод обновленного списка фондов
# print(funds)

with open('data_dom_date.json', 'w') as file:
    json.dump(funds, file)



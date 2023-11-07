from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
import requests
from auth_tg import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

headers = {
    'authority': 'www.olx.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'dfp_user_id=abc7d3e4-8a3b-4a2b-8460-5f6f35316ddb-ver2; __utmz=250720985.1693940545.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _hjid=85037f38-e958-497a-847f-cee276fc1fbd; _hjSessionUser_2218922=eyJpZCI6IjBlZWI2MmUwLTAwMmEtNWFmNi04YWM0LWFjYzNkM2QwMjA1NiIsImNyZWF0ZWQiOjE2OTM5NDA1NDQ4MzIsImV4aXN0aW5nIjp0cnVlfQ==; deviceGUID=cf9e27e3-c986-4eaf-951b-04ef6fc8b77f; a_grant_type=device; user_business_status=private; __diug=true; cookieBarSeenV2=true; cookieBarSeen=true; _pbjs_userid_consent_data=3524755945110770; _sharedid=11443fef-aa93-4583-9ed1-50f3c13af610; _gcl_au=1.1.1969239140.1693940711; __gsas=ID=55453635838f0d36:T=1693941647:RT=1693941647:S=ALNI_MYVwnR24OcEsEmAyrSL9nPkjeCKJA; lang=ru; _gac_UA-124076552-2=1.1694204397.CjwKCAjwjOunBhB4EiwA94JWsNIcjwZ-0DHJkdrnuU6wnZppa9WiHPOLKnEu7Nt0qOIucyNy_EwItBoCQ0gQAvD_BwE; cto_bundle=vq55Kl9IZk1mbDh6cVk5Q2NJTU9IMCUyQkRObjlBU0YzU2oxNGl3YWE0JTJCdnlBRXYlMkZlWXpiVG5ON1gzTGowdWVSZ2h1YlBBckl6MCUyRkowTDU0T3RQaUthZkpFUzRqMXAlMkJ6VERVVVdLOHRzWGpIU0hHJTJGWk9tYWRtMkFBNzJaYk1DVnJKVGlRNmZhZ3lCYkZpJTJGQ0tpRG9KSWIwN3RuUSUzRCUzRA; cto_bidid=czISLF9uNVhhVjFRb1RUTUxoa3F3eWtYSmRsOWdmTG5NSTBoN21hMXpDTXBHVnFEVjZOMlpCSFdMdDZ6WmlRaFd3VHhWJTJCUDdiWVRTQ25BR2NBcVBNT21RUjdvQ29RZmZ2MVFmdDI0Um55VHFjQzd3JTNE; _sharedid=51a7da43-ef85-4f6a-8178-eb02df5be4ea; a_refresh_token=47d5815824c01ff4497484e9be3da804614ff4fd; laquesissu=298@reply_chat_sent|1#302@jobs_applications|0#600@my_messages_sent|1#663@jobs_homepage_survey_trigger|0; observed_aui=e5c5142d65444ba1975359552ab12329; user_id=1158854616; __user_id_P&S=1158854616; user_uuid=; mobile_default=desktop; fingerprint=MTI1NzY4MzI5MTsxNjswOzA7MDsxOzA7MDswOzA7MDsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MDsxOzE7MTswOzA7MTswOzE7MTsxOzE7MTsxOzE7MTswOzE7MTswOzE7MTsxOzA7MDswOzA7MDswOzE7MDsxOzE7MDswOzA7MDswOzA7MTsxOzA7MTsxOzE7MTswOzE7MDsyOTgyOTUwNTY5OzI7MjsyOzI7MjsyOzU7Mjg0ODAwNjQxODsxMzU3MDQxNzM4OzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzA7MDszNTYzNjM2Njc7MzQ2OTMwNjU1MTsyNDIyNDE5MzgxOzc4NTI0NzAyOTsxMDA1MzAxMjAzOzE5MjA7MTA4MDsyNDsyNDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzA7MDsw; from_detail=0; _hjIncludedInSessionSample_2218922=0; __utma=250720985.1806835627.1693940545.1698424694.1698867856.38; __utmc=250720985; _gid=GA1.2.23732966.1698867856; laquesis=deluareb-2631@b#er-2488@a#er-2542@a#er-2577@b#erm-1299@a#erm-1348@b#jobs-6094@b#olxeu-41244@b#posting-1090@a#recs-10@b; my_city_2=334_0_0_%D0%9A%D1%80%D0%B0%D1%81%D0%B8%D0%BB%D0%BE%D0%B2_0_%D0%A5%D0%BC%D0%B5%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C_krasilov; a_access_token=fc354b6eb0cdf2439279dbed8fd5efa26a715352; laquesisff=aut-1425#aut-388#buy-2279#de-1934#decision-657#euonb-114#grw-124#kuna-307#oesx-1437#oesx-2630#oesx-2797#oesx-2798#oesx-2864#oesx-2926#oesx-3343#oesx-645#oesx-867#ser-126#ser-311#ser-386#ser-429#ser-80#ser-87#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-682; _hjSession_2218922=eyJpZCI6IjQ3YTZhMGNmLTc5ZDMtNGMyMC04NjlkLWUyMDJhNGI4MjgwMyIsImNyZWF0ZWQiOjE2OTg4NzMyNTg5MTksImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6ZmFsc2V9; PHPSESSID=edtlgs3o1bmhllbd9ss2e6lm7i; dfp_segment=%5B%5D; delivery_l1=transport; cto_bidid=nvjuv19uNVhhVjFRb1RUTUxoa3F3eWtYSmRsOWdmTG5NSTBoN21hMXpDTXBHVnFEVjZOMlpCSFdMdDZ6WmlRaFd3VHhWJTJCUDdiWVRTQ25BR2NBcVBNT21RUjdwJTJCUmtaZWVpMjdxMkxiYVRlRHdmbTglM0Q; cto_bidid=nvjuv19uNVhhVjFRb1RUTUxoa3F3eWtYSmRsOWdmTG5NSTBoN21hMXpDTXBHVnFEVjZOMlpCSFdMdDZ6WmlRaFd3VHhWJTJCUDdiWVRTQ25BR2NBcVBNT21RUjdwJTJCUmtaZWVpMjdxMkxiYVRlRHdmbTglM0Q; session_start_date=1698875423155; cto_bundle=yqgDQl9IZk1mbDh6cVk5Q2NJTU9IMCUyQkRObjU0WU52QWd2VGgxUlBZNDZCJTJCbEozZWI0QyUyQlV5NktEdHpDQjBkZ2R6VGVQdU5uNWhrbUhURzFjNm5DTmZuTGlqMm5YSkdLWXFQeVA3NlRVMVNSamE3bCUyRkZ2YkpBNjklMkZsaUV5d21vTVBSUHNKRWRLUFBscThmQ2ZBVDVVdDBQZFJ3TDNteG1VNW4zZVRJRVQlMkZMNVg4V3ZmejFuT3BNa1lXaHRCZ2pUTjFMcXNGMDZsRjVOa2hiZHcyVmlRcGQ3V0NBJTNEJTNE; cto_bundle=yqgDQl9IZk1mbDh6cVk5Q2NJTU9IMCUyQkRObjU0WU52QWd2VGgxUlBZNDZCJTJCbEozZWI0QyUyQlV5NktEdHpDQjBkZ2R6VGVQdU5uNWhrbUhURzFjNm5DTmZuTGlqMm5YSkdLWXFQeVA3NlRVMVNSamE3bCUyRkZ2YkpBNjklMkZsaUV5d21vTVBSUHNKRWRLUFBscThmQ2ZBVDVVdDBQZFJ3TDNteG1VNW4zZVRJRVQlMkZMNVg4V3ZmejFuT3BNa1lXaHRCZ2pUTjFMcXNGMDZsRjVOa2hiZHcyVmlRcGQ3V0NBJTNEJTNE; onap=18a66b97466x333a131b-57-18b8cbcbad1x6fde09c1-26-1698875424; _ga=GA1.1.1806835627.1693940545; _ga_TVZPR1MEG9=GS1.1.1698873261.60.1.1698873627.46.0.0; lqstatus=1698877424|18b8cbcbad1x6fde09c1|er-2488||; __gads=ID=59153bcdbabc7de0:T=1693940546:RT=1698876526:S=ALNI_MbA461CFzGRrjSmcZlXk5xSr9PDpQ; __gpi=UID=00000c6f3b6d098c:T=1693940546:RT=1698876526:S=ALNI_MbLKoP1yjJjpM_cDyCtPpN8tT8CyA',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://www.olx.ua/transport/legkovye-avtomobili/krasilov/?currency=USD&search%5Border%5D=created_at:desc',
    headers=headers,
    )

html_content = response.content


soup = BeautifulSoup(html_content, 'html.parser')

listing_grid = soup.find('div', {'data-testid': 'listing-grid'})

cards_ad = listing_grid.find_all(
    'div', {'data-cy': 'l-card', 'data-testid': 'l-card'})
# Then, iterate over all the child divs with the specified attributes and classes
links = []
for div in cards_ad:
    link = div.find('a', {'class': 'css-rc5s2u'}).get('href')
    links.append('https://www.olx.ua/'+link)

# print(links)

# for link in links:
link = 'https://www.olx.ua/d/obyavlenie/prodam-bmw-e39-528i-IDSCprY.html'
response = requests.get(
    link,
    headers=headers,
)
adv_html = response.content

adv_content = BeautifulSoup(adv_html, 'html.parser')

# Знаходимо всі елементи <li> в межах <ol> з конкретним data-testid
breadcrumb_items = adv_content.find_all('li', attrs={"data-testid": "breadcrumb-item"})

# Отримуємо четвертий елемент, якщо він існує
car_brand = breadcrumb_items[3].get_text(strip=True) if len(breadcrumb_items) > 3 else None

adv_param = adv_content.find('ul',class_='css-sfcl1s')
# print(adv_param)
# Шукаємо всі елементи li з певним класом
items = adv_param.find_all('li', class_='css-1r0si1e')

# Витягуємо потрібну інформацію
for item in items:
    text = item.get_text(strip=True)
    if "VIN номер:" in text:
        vin = text.split(': ')[1]
    elif "Держ. номер реєстрації:" in text:
        registration_number = text.split(': ')[1]
    elif "Модель:" in text:
        model = text.split(': ')[1]
    elif "Рік випуску:" in text:
        year_of_manufacture = text.split(': ')[1]
    elif "Пробіг:" in text:
        mileage = text.split(': ')[1]
    elif "Вид палива:" in text:
        fuel_type = text.split(': ')[1]
    elif "Об'єм двигуна:" in text:
        engine_capacity = text.split(': ')[1]

# Виводимо інформацію

async def send_advert(message: types.Message):
    await message.answer(
        f'❗️Нове оголошення на OLX: {link}\n'
        f'🚙Автомобіль: {car_brand} {model}\n'
        f'🕰Рік випуску: {year_of_manufacture}\n'
        f'🎈Об\'єм двигуна: {engine_capacity}\n'
        f'⛽️Вид палива: {fuel_type}\n'
        f'🚕Пробіг: {mileage}\n'
        f'#️⃣VIN: {vin}\n'
        f'🆔Номер авто: {registration_number}'
        
        f'Price: '
    )
# Хендлер для команди старту /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Надішліть мені команду /advert і я відправлю інформацію про оголошення.")

# Хендлер для команди /advert, який викликає функцію send_advert
@dp.message_handler(commands=['advert'])
async def advert_command(message: types.Message):
    await send_advert(message)

# Запускаємо довготривалий процес опитування бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
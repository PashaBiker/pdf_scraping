from openbb_terminal.sdk import openbb
f = openbb.funds.load("F000013GO6", 'gb',)
# Получение исторических данных
historical_data = openbb.funds.historical(f, "20/11/1980", "20/11/2023")

# Сохранение данных в файл в формате CSV
historical_data.to_excel("F000013GO6.xlsx")
print('finished')
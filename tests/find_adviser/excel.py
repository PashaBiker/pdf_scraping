import json
import pandas as pd

# Загрузите данные из JSON файла
with open("tests/find_adviser/final_result.json", "r") as file:
    data = json.load(file)

# Преобразуйте список словарей в датафрейм pandas
df = pd.DataFrame(data)

# Сохраните датафрейм в файл Excel
df.to_excel("tests/find_adviser/output_file.xlsx", index=False)

import json

# Шаг 1: Прочтите содержимое файла
with open("tests/find_adviser/final.json", "r") as file:
    data = json.load(file)

# Шаг 2: Преобразуйте список словарей в список кортежей
unique_data = list({tuple(item.items()): item for item in data}.values())

# Шаг 3: Сохраните уникальные данные обратно в файл
with open("tests/find_adviser/final_result.json", "w") as file:
    json.dump(unique_data, file, indent=4)
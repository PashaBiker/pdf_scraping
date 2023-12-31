







import re

from PyPDF2 import PdfReader
import pdfplumber

def get_data_addition(pdf):
    def extract_top_left_text(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            
            # Use enumerate to get the page index
            for i, page in enumerate(pdf.pages):
                # Check if the page is one of 1, 4, 8, etc. (keeping in mind that indices start from 0)
                if (i+1) % 4 != 1:
                    continue

                # Calculate dimensions for the top-left quadrant
                x0, top, x1, bottom = page.bbox
                width = x1 - x0
                height = bottom - top

                crop_box = (x0, top, x0 + width * 0.5, top + height * 0.5)
                
                # Crop the page to the top-left quadrant and extract text
                cropped_page = page.crop(bbox=crop_box)
                all_text += cropped_page.extract_text() + "\n"

        return all_text.strip().split('\n')

    # Example
    text = extract_top_left_text(pdf)

    assets_categories = ['Equity', 'Fixed Income', 'Cash', 'Multi Asset ', 'Alternatives']
    assets_groups = []
    assets_current_group = []
    found_assets_holdings = False

    for i, line in enumerate(text):
        if 'ASSET CLASS' in line :
            found_assets_holdings = True
            continue  # Пропускаем текущую строку, чтобы она не добавлялась в current_group

        # Если находим строку 'Important Information', останавливаем добавление
        elif 'OBJECTIVES AND POLICY' in line:
            found_assets_holdings = False
            
            if assets_current_group:
                assets_groups.append(assets_current_group)
                # print(groups)
                assets_current_group = []

        # Если мы внутри интересующего нас блока, добавляем строки
        elif found_assets_holdings:
            assets_current_group.append(line.strip())
        assets_categories_pattern = "|".join(assets_categories)

        assets_result = []
    # print(current_group)
    for group in assets_groups:
        i = 0
        while i < len(group):
            if i < len(group) - 1 and "Fixed Income Multi Asset" in group[i] and group[i + 1] == "Credit":
                percentage_part = group[i].split('Fixed Income Multi Asset ')[1]
                group[i] = 'Fixed Income Multi Asset Credit ' + percentage_part
                group.pop(i + 1)
            i += 1  
            
    # print(groups, '-- groups \n')
    for lst in assets_groups:
        category_values = []
        # Сombine all in one string
        joined_string = " ".join(lst)
        # Ищем все вхождения категорий в объединенной строке
        for match in re.finditer(assets_categories_pattern, joined_string):
            category = match.group(0)  # Получаем название категории
            # Получаем подстроку после найденной категории
            string_after_category = joined_string[match.end():]
            # Ищем первое число в подстроке (значение категории)
            value_match = re.search(r'\b\d+(\.\d+)?', string_after_category)
            if value_match:
                value = value_match.group(0)  # Получаем значение
                # Добавляем категорию и значение в список
                category_values.append(f"{category} {value}%")
        assets_result.append(category_values)

    for i in range(len(assets_result)):
        assets_result[i] = list(dict.fromkeys(assets_result[i]))
    # print('\n'*2, result, '-- result \n')
    assets_grouped_assets = []
    for group in assets_result:
        keys = []
        values = []
        for line in group:
            key, value = line.rsplit(' ', 1)  # Разделяем строку на две части по последнему пробелу
            keys.append(key)
            values.append(value)
        assets = dict(zip(keys, values))
        assets_grouped_assets.append(assets)
    return assets_grouped_assets

def get_data(file):


    filenames = []
    date = []
    ongoing_costs = []
    one_month = []
    one_year = []

    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text(use_text=True)
        text = text.split('\n')
        # print(text)
        # breakpoint()
        for i, line in enumerate(text):
            if i == 0:
                filenames.append(text[0])
            elif i == len(text) - 1:
                continue
            else:
                if '4 of 4' in line:
                    filenames.append(line.split('4 of 4')[-1].strip())

        # print(filenames)
        for i,line in enumerate(text):
            if 'Ongoing Costs' in line:
                oc_match = re.search(r'(\d+\.\d+)', line)
                ongoing_costs.append(oc_match.group(1))
                date.append(text[1])
            if "Time Period" in line:
                # print(text[i+1])
                values_line = text[i+1]
                values = re.findall(r'(-?\d+\.\d+)%', values_line)
                one_month.append(float(values[0]))
                one_year.append(float(values[3]))
            

    print(filenames)
    print(date)
    print(ongoing_costs)
    print(one_month)
    print(one_year)

    unsorted_categories = [
        'Global Equities',
        'Corporate Bonds',
        'Global Multi Asset',
        'UK Equities',
        'Cash',
        'Alternatives',
        'Asia Pacific Ex Japan Equities',
        'European Equities',
        'Fixed Income Multi Asset',
        'Fixed Income Multi Asset Credit',
        'Japanese Equities',   
        'Emerging Market Equities',
        'Global Government Bonds',
        'US Equities',
    ]

    categories = sorted(unsorted_categories, key=lambda x: len(x), reverse=True)

    groups = []
    current_group = []
    found_portfolio_holdings = False

    for i, line in enumerate(text):
        if 'WEIGHTS BY ASSET' in line :
            found_portfolio_holdings = True
            continue  # Пропускаем текущую строку, чтобы она не добавлялась в current_group

        # Если находим строку 'Important Information', останавливаем добавление
        elif 'TOP 10 PERFORMANCE CONTRIBUTORS OVER 1 YEAR' in line:
            found_portfolio_holdings = False
            
            if current_group:
                groups.append(current_group)
                # print(groups)
                current_group = []

        # Если мы внутри интересующего нас блока, добавляем строки
        elif found_portfolio_holdings:
            current_group.append(line.strip())
        categories_pattern = "|".join(categories)

        result = []
    # print(current_group)
    for group in groups:
        i = 0
        while i < len(group):
            if i < len(group) - 1 and "Fixed Income Multi Asset" in group[i] and group[i + 1] == "Credit":
                percentage_part = group[i].split('Fixed Income Multi Asset ')[1]
                group[i] = 'Fixed Income Multi Asset Credit ' + percentage_part
                group.pop(i + 1)
            i += 1  
            
    # print(groups, '-- groups \n')
    for lst in groups:
        category_values = []
        # Сombine all in one string
        joined_string = " ".join(lst)
        # Ищем все вхождения категорий в объединенной строке
        for match in re.finditer(categories_pattern, joined_string):
            category = match.group(0)  # Получаем название категории
            # Получаем подстроку после найденной категории
            string_after_category = joined_string[match.end():]
            # Ищем первое число в подстроке (значение категории)
            value_match = re.search(r'\b\d+(\.\d+)?', string_after_category)
            if value_match:
                value = value_match.group(0)  # Получаем значение
                # Добавляем категорию и значение в список
                category_values.append(f"{category} {value}%")
        result.append(category_values)

    for i in range(len(result)):
        result[i] = list(dict.fromkeys(result[i]))
    # print('\n'*2, result, '-- result \n')
    grouped_assets = []
    for group in result:
        keys = []
        values = []
        for line in group:
            key, value = line.rsplit(' ', 1)  # Разделяем строку на две части по последнему пробелу
            keys.append(key)
            values.append(value)
        assets = dict(zip(keys, values))
        grouped_assets.append(assets)

    print(grouped_assets)


    def merge_lists(list1, list2):
        # Initialize an empty list to store the merged dictionaries
        merged_list = []

        # Loop over pairs of dictionaries from list1 and list2
        for dict1, dict2 in zip(list1, list2):
            # Create a copy of the dictionary from list1 to avoid modifying the original
            merged_dict = dict1.copy()
            
            # Update the merged dictionary with key-value pairs from dict2, only if the key doesn't exist in dict1
            for key, value in dict2.items():
                if key not in merged_dict:
                    merged_dict[key] = value

            # Add the merged dictionary to the merged list
            merged_list.append(merged_dict)

        return merged_list
    
    assets_grouped_assets = get_data_addition(file)
    combined_list = merge_lists(assets_grouped_assets, grouped_assets)
    print(combined_list)

    for i, filename  in enumerate(filenames):
        result[i] = {
            'Date': date[i],
            'Ongoing Costs*': ongoing_costs[i],
            '1yr': one_year[i],
            '1m': one_month[i],
            'Assets': combined_list[i]
        }
        print(
            'Date', date[i], "\n",
            'One month', one_month[i],"\n",
            '12 months', one_year[i],"\n",
            'Ongoing Costs', ongoing_costs[i],"\n",
            'Assets', combined_list[i],"\n",
            )
    # print(result)
    
    return result

if __name__ == "__main__":
    file = '16_milestone\Trust DFM\Trust DFM PDFs\Flourish.pdf'
    get_data(file)
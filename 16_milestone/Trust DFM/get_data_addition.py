import re
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

pdf_path = "16_milestone\Trust DFM\Trust DFM PDFs\Flourish.pdf"

get_data_addition(pdf_path)
print()
data2 = [{'Global Equities': '23.90%', 'Corporate Bonds': '16.70%', 'UK Equities': '16.10%', 'Cash': '10.00%', 'Fixed Income Multi Asset': '7.30%', 'Asia Pacific Ex Japan Equities': '5.00%', 'US Equities': '2.80%', 'Japanese Equities': '2.30%', 'Alternatives': '2.30%', 'Fixed Income Multi Asset Credit': '2.00%'}, {'Global Equities': '26.50%', 'UK Equities': '19.70%', 'Corporate Bonds': '14.70%', 'Cash': '8.80%', 'Asia Pacific Ex Japan Equities': '6.30%', 'Fixed Income Multi Asset': '6.00%', 'Global Multi Asset': '4.40%', 'Japanese Equities': '3.20%', 'Alternatives': '2.20%', 'US Equities': '2.20%'}, {'European Equities': '1.00%', 'Alternatives': '2.00%', 'Fixed Income Multi Asset Credit': '3.00%', 'Fixed Income Multi Asset': '10.10%', 'Global Multi Asset': '11.00%', 'Cash': '14.30%', 'Corporate Bonds': '17.90%', 'UK Equities': '20.20%', 'Global Equities': '20.50%'}, {'Global Equities': '30.00%', 'UK Equities': '20.50%', 'Corporate Bonds': '12.50%', 'Asia Pacific Ex Japan Equities': '7.50%', 'European Equities': '7.00%', 'US Equities': '4.00%', 'Fixed Income Multi Asset': '4.00%', 'Japanese Equities': '3.50%', 'Global Multi Asset': '3.00%', 'Alternatives': '1.50%'}, {'Global Equities': '33.50%', 'UK Equities': '21.10%', 'Corporate Bonds': '10.30%', 'Asia Pacific Ex Japan Equities': '8.70%', 'European Equities': '8.00%', 'Cash': '4.20%', 'Japanese Equities': '3.80%', 'Fixed Income Multi Asset': '2.00%', 'Global Multi Asset': '1.60%', 'Alternatives': '0.80%'}, {'European Equities': '0.50%', 'Alternatives': '1.00%', 'Fixed Income Multi Asset Credit': '1.50%', 'Fixed Income Multi Asset': '8.10%', 'Global Multi Asset': '9.90%', 'Cash': '13.00%', 'Corporate Bonds': '14.30%', 'Global Equities': '24.90%', 'UK Equities': '26.80%'}, {'European Equities': '1.50%', 'Alternatives': '3.00%', 'Fixed Income Multi Asset Credit': '4.50%', 'Global Multi Asset': '12.00%', 'Fixed Income Multi Asset': '12.00%', 'UK Equities': '13.60%', 'Cash': '15.70%', 'Global Equities': '16.30%', 'Corporate Bonds': '21.40%'}, {'European Equities': '2.00%', 'Alternatives': '4.00%', 'Fixed Income Multi Asset Credit': '6.00%', 'UK Equities': '7.00%', 'Global Equities': '12.00%', 'Global Multi Asset': '13.00%', 'Fixed Income Multi Asset': '14.00%', 'Cash': '17.00%', 'Corporate Bonds': '25.00%'}, {'Global Equities': '23.00%', 'UK Equities': '19.00%', 'Corporate Bonds': '17.00%', 'Cash': '11.00%', 'Fixed Income Multi Asset': '8.00%', 'Global Multi Asset': '6.00%', 'Asia Pacific Ex Japan Equities': '5.00%', 'European Equities': '5.00%', 'Japanese Equities': '3.00%', 'Alternatives': '3.00%'}, {'Cash': '2.00%', 'Japanese Equities': '4.00%', 'US Equities': '8.00%', 'Corporate Bonds': '8.00%', 'European Equities': '9.00%', 'Asia Pacific Ex Japan Equities': '10.00%', 'UK Equities': '22.00%', 'Global Equities': '37.00%'}]
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

combined_list = merge_lists(assets_grouped_assets, data2)
print(combined_list)
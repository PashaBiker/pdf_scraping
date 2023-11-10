import glob
import pdfplumber
import re
# Путь к вашему PDF-файлу
pdf_path = '19_milestone\Rayner Spencer Mills Research Limited\Rayner Spencer Mills Research Limited PDFs\Responsible Balanced.pdf'

# Открываем PDF-файл
def get_charges(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Получаем вторую страницу (нумерация начинается с 0)
        page = pdf.pages[1]

        # Определяем границы для обрезки страницы (70% слева будут отброшены)
        width = page.width
        height = page.height
        left = width * 0.7  # 70% ширины страницы
        top = 0
        right = width
        bottom = height

        # Обрезаем страницу и извлекаем текст с правой части
        cropped_page = page.within_bbox((left, top, right, bottom))
        text = cropped_page.extract_text()
        text = text.split('\n')
        for line in text:
            if '(no VAT)' in line:
                DFM = re.search(r'\d.\d\d%', line).group(0).replace('%','')
                print(DFM)
            if 'KIID Ongoing Charge' in line:
                OCF = re.search(r'\d.\d\d', line).group(0).replace('%','')
                print(OCF)

    return  DFM, OCF

def get_assets(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Получаем вторую страницу (нумерация начинается с 0)
        page = pdf.pages[1]

        # Определяем границы для обрезки страницы (70% слева будут отброшены)
        width = page.width
        height = page.height
        left = 0
        top = 0
        right = width * 0.7  # 70% ширины страницы
        bottom = height * 0.5

        # Обрезаем страницу и извлекаем текст с левой части
        cropped_page = page.within_bbox((left, top, right, bottom))
        text = cropped_page.extract_text()
        text = text.split('\n')
        # print(text)

        asset_labels = ['Equities',	
        'Fixed Income',	
        'Cash/Money Market',	
        'Other',]
        asset_percentages = {}

        # Loop through each asset label and find the corresponding percentage in the text
        for asset in asset_labels:
            # Create a pattern to find the asset followed by its percentage
            pattern = rf"{asset}\s+(\d+\.\d+)"
            
            # Search the text for the pattern
            for line in text:
                match = re.search(pattern, line)
                if match:
                    # If found, add the asset and percentage to the dictionary
                    asset_percentages[asset] = float(match.group(1))

        print(asset_percentages)
        total_percentage = sum(asset_percentages.values())

        print(total_percentage)  # This will output the sum of the values


def get_year_date(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Получаем вторую страницу (нумерация начинается с 0)
        page = pdf.pages[0]

        # Определяем границы для обрезки страницы (70% слева будут отброшены)
        width = page.width
        height = page.height
        left = 0
        top = 0
        right = width * 0.625  # 70% ширины страницы
        bottom = height

        # Обрезаем страницу и извлекаем текст с левой части
        cropped_page = page.within_bbox((left, top, right, bottom))
        text = cropped_page.extract_text()
        text = text.split('\n')
        # print(text)
        for line in text:
            if 'As of' in line:
                date_pattern = r"\b(\d{2}/\d{2}/\d{4})\b"

                # Search for the pattern in the text
                match = re.search(date_pattern, line)
                date = match.group(1)
                print(date)

            pattern = r"-?\d+\.\d+"
            matches = re.findall(pattern, line)
            # Check if there are more than three such matches
            if len(matches) > 3:
                print(f"Found line: {line}")
                # Pattern to match numbers with an optional minus, digits, a dot, and digits
                pattern = r"(-?\d+\.\d+|—)"

                # Find all matches
                matches = re.findall(pattern, line)

                # Function to convert matches to float or None
                def convert_value(value):
                    return float(value) if value != '—' else None

                # Check if we have enough values to extract the ones we are interested in
                if len(matches) >= 6:
                    one_month = convert_value(matches[0])  # The first value is the one-month value
                    one_year = convert_value(matches[2])  # The third value is the one-year value
                    three_years = convert_value(matches[3])  # The fourth value is the three-years value, here will be None
                    five_years = convert_value(matches[4]) 

                    print(one_month,
                        one_year,
                        three_years,
                        five_years,)
                break  
    return date, one_month, one_year, three_years, five_years

if __name__ == '__main__':
    # get_year_date(pdf_path)
    pdfs = glob.glob('19_milestone\Rayner Spencer Mills Research Limited\Rayner Spencer Mills Research Limited PDFs' + '/*.pdf')
    for pdf in pdfs:
        get_year_date(pdf)
        get_charges(pdf)
        get_assets(pdf)

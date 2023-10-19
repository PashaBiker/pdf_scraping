







import re

from PyPDF2 import PdfReader
import pdfplumber


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
        

    # print(filenames)
    # print(date)
    # print(ongoing_costs)
    # print(one_month)
    # print(one_year)

    categories = [
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

    groups = []
    current_group = []
    found_portfolio_holdings = False

    i = 0
    while i < len(text):
        line = text[i]
        # Combine 'Fixed Income Multi Asset' with 'Credit' when they are consecutive
        if "Fixed Income Multi Asset" in line and (i + 1) < len(text) and text[i + 1] == "Credit":
            line = "Fixed Income Multi Asset Credit"
            i += 1  # Skip next iteration

        if 'WEIGHTS BY ASSET' in line:
            found_portfolio_holdings = True
        elif 'TOP 10 PERFORMANCE CONTRIBUTORS OVER 1 YEAR' in line:
            found_portfolio_holdings = False
            if current_group:
                groups.append(current_group)
                current_group = []
        elif found_portfolio_holdings:
            current_group.append(line.strip())
        i += 1

    categories_pattern = "|".join(categories)
    result = []

    for lst in groups:
        category_values = []
        joined_string = " ".join(lst)
        for match in re.finditer(categories_pattern, joined_string):
            category = match.group(0)
            string_after_category = joined_string[match.end():]
            value_match = re.search(r'\b\d+(\.\d+)?%', string_after_category)
            if value_match:
                value = value_match.group(0)
                category_values.append(f"{category} {value}")
        result.append(category_values)

    for i in range(len(result)):
        result[i] = list(dict.fromkeys(result[i]))

    grouped_assets = []
    for group in result:
        keys = []
        values = []
        for line in group:
            key, value = line.rsplit(' ', 1)
            keys.append(key)
            values.append(value)
        assets = dict(zip(keys, values))
        grouped_assets.append(assets)

    print(grouped_assets)
    # for i in enumerate(filenames):
    #     result[i] = {
    #         'Date': date[i],
    #         'Ongoing Costs*': ongoing_costs[i],
    #         '1yr': one_year[i],
    #         '1m': one_month[i],
    #         'Assets': grouped_assets[i]
    #     }
    #     print(
    #         'Date', date[i], "\n",
    #         'One month', one_month[i],"\n",
    #         '12 months', one_year[i],"\n",
    #         'Ongoing Costs', ongoing_costs[i],"\n",
    #         'Assets', grouped_assets[i],"\n",
    #         )
    
    return result

if __name__ == "__main__":
    file = '16_milestone\Trust DFM\Trust DFM PDFs\Flourish.pdf'
    get_data(file)
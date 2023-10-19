import re

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

text = [
    'European Equities 1.00%',
    'Alternatives 2.00%',
    'Fixed Income Multi Asset 3.00%',
    'Credit',
    'Fixed Income Multi Asset 10.10%',
    'Global Multi Asset 11.00%',
    'Cash 14.30%',
    'Corporate Bonds 17.90%',
    'UK Equities 20.20%',
    'Global Equities 20.50%',
    '0% 5% 10% 15% 20% 25%'
]

groups = []
current_group = []
found_portfolio_holdings = True  # Set to True for the provided example

for i, line in enumerate(text):
    if 'Credit' in line and 'Fixed Income Multi Asset' in current_group[-1]:
        current_group[-1] += ' ' + line
    else:
        current_group.append(line.strip())

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

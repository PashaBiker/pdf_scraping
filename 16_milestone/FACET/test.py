import re

data1 = 'point on 30th June 2023 (except where indicated)'
data2 = 'Information in this factsheet is at the last valuation point on 31st August 2023 (except where indicated).'
data = ['Information in this factsheet is at the last valuation point on 31tst August 2023 (except where indicated).']
def clean_date(data):
    match = re.search(r'(\d+)(st|nd|rd|th|tst) (\w+ \d+)', data)
    if match:
        day = match.group(1)
        month_year = match.group(3)
        return f"{day} {month_year}"
    return None

for line in data:
    if 'except where indicated' in line:
        date = clean_date(line)


print(date)  # 30 June 2023

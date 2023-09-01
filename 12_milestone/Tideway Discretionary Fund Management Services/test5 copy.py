lines = [
    'Short-Dated Fixed Income ',
    '(<5 years)',
    'Fixed Income (>5 years)',
    'Alternatives',
    'Equity Income',
    'Equity Growth',
    'Portfolios are managed by Tideway Investment Partners LLP on b',
    'Wealth Management Ltd.',
    '© 2019 Tideway Investment Partners LLP. This document has be',
    'and issued by Tideway Investment Partners LLP. Tideway Wealth ',
    'Limited is an appointed representative of Tideway Investment Pa',
    'which is authorised and regulated by the Financial Conduct Autho',
    'number: 496214.',
    'Performance Line Chart ',
    'Pricing Spread: Bid-Bid ● Data Frequency: Daily ● Currency: Pounds Sterling',
    'The value of units can fall as well as rise.',
    'Past performance should not be seen as an indication of future performance',
    '33.75%',
    '21.25%',
    '22%',
    '14.63%',
    '10.38%',
]

asset_name = []
asset_val = []

is_asset = True

for line in reversed(lines):
    if line.strip() and line[0].isalpha() and is_asset == False:
        break
    if line.strip() and line[0].isalpha() and is_asset == True:
        asset_name.append(line.strip())
        continue
    if line.strip() and line[-1] == "%":
        asset_val.append(line.strip().replace('%',''))
        is_asset = False
        continue

# Чтобы соответствовать вашему ожидаемому результату, инвертируем списки
asset_name = asset_name[::-1]
asset_val = asset_val[::-1]

assets = dict(zip(asset_name, asset_val))
print(assets)

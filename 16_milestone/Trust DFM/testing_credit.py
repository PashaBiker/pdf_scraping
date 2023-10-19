






groups = [

  [
    'Global Equities 23.90%',
    'Corporate Bonds 16.70%',
    'UK Equities 16.10%',
    'Cash 10.00%',
    'Fixed Income Multi Asset 7.30%',
    '0% 5% 10% 15% 20% 25%',
    'Asia Pacific Ex Japan Equities 5.00%',
    'US Equities 2.80%',
    'Japanese Equities 2.30%',
    'Alternatives 2.30%',
    'Fixed Income Multi Asset 2.00%',
    'Credit',
    '0% 1% 2% 3% 4% 5%'
  ],
  [
    'Global Equities 26.50%',
    'UK Equities 19.70%',
    'Corporate Bonds 14.70%',
    'Cash 8.80%',
    'Asia Pacific Ex Japan Equities 6.30%',
    '0% 10% 20% 30%',
    'Fixed Income Multi Asset 6.00%',
    'Global Multi Asset 4.40%',
    'Japanese Equities 3.20%',
    'Alternatives 2.20%',
    'US Equities 2.20%',
    '0% 2% 4% 6%'
  ],
  [
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
  ],
  [
    'Global Equities 30.00%',
    'UK Equities 20.50%',
    'Corporate Bonds 12.50%',
    'Asia Pacific Ex Japan Equities 7.50%',
    'European Equities 7.00%',
    '0% 10% 20% 30%',
    'US Equities 4.00%',
    'Fixed Income Multi Asset 4.00%',
    'Japanese Equities 3.50%',
    'Global Multi Asset 3.00%',
    'Alternatives 1.50%',
    '0% 1% 2% 3% 4%'
  ],
  [
    'Global Equities 33.50%',
    'UK Equities 21.10%',
    'Corporate Bonds 10.30%',
    'Asia Pacific Ex Japan Equities 8.70%',
    'European  Equities 8.00%',
    '0% 10% 20% 30% 40%',
    'Cash 4.20%',
    'Japanese Equities 3.80%',
    'Fixed Income Multi Asset 2.00%',
    'Global Multi Asset 1.60%',
    'Alternatives 0.80%',
    '0% 1% 2% 3% 4% 5%'
  ],
  [
    'European Equities 0.50%',
    'Alternatives 1.00%',
    'Fixed Income Multi Asset 1.50%',
    'Credit',
    'Fixed Income Multi Asset 8.10%',
    'Global Multi Asset 9.90%',
    'Cash 13.00%',
    'Corporate Bonds 14.30%',
    'Global Equities 24.90%',
    'UK Equities 26.80%',
    '0% 10% 20% 30%'
  ],
  [
    'European Equities 1.50%',
    'Alternatives 3.00%',
    'Fixed Income Multi Asset 4.50%',
    'Credit',
    'Global Multi Asset 12.00%',
    'Fixed Income Multi Asset 12.00%',
    'UK Equities 13.60%',
    'Cash 15.70%',
    'Global Equities 16.30%',
    'Corporate Bonds 21.40%',
    '0% 5% 10% 15% 20% 25%'
  ],
  [
    'European Equities 2.00%',
    'Alternatives 4.00%',
    'Fixed Income Multi Asset 6.00%',
    'Credit',
    'UK Equities 7.00%',
    'Global Equities 12.00%',
    'Global Multi Asset 13.00%',
    'Fixed Income Multi Asset 14.00%',
    'Cash 17.00%',
    'Corporate Bonds 25.00%',
    '0% 5% 10% 15% 20% 25%'
  ],
  [
    'Global Equities 23.00%',
    'UK Equities 19.00%',
    'Corporate Bonds 17.00%',
    'Cash 11.00%',
    'Fixed Income Multi Asset 8.00%',
    '0% 5% 10% 15% 20% 25%',
    'Global Multi Asset 6.00%',
    'Asia Pacific Ex Japan Equities 5.00%',
    'European Equities 5.00%',
    'Japanese Equities 3.00%',
    'Alternatives 3.00%',
    '0% 2% 4% 6%'
  ],
  [
    'Cash 2.00%',
    'Japanese Equities 4.00%',
    'US Equities 8.00%',
    'Corporate Bonds 8.00%',
    'European Equities 9.00%',
    'Asia Pacific Ex Japan Equities 10.00%',
    'UK Equities 22.00%',
    'Global Equities 37.00%',
    '0% 10% 20%  30% 40%'
  ]
]



for group in groups:
    i = 0
    while i < len(group):
        if i < len(group) - 1 and "Fixed Income Multi Asset" in group[i] and group[i + 1] == "Credit":
            percentage_part = group[i].split('Fixed Income Multi Asset ')[1]
            group[i] = 'Fixed Income Multi Asset Credit ' + percentage_part
            group.pop(i + 1)
        i += 1

print(groups)
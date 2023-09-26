assets_labels = ['Short-Dated', 'Equity Growth', 'Equity Income', 'Alternatives', 'Fixed Income']
tags_found = ['Equity Income', 'Equity Growth']
percentages = ['41.50%', '58.50%']

# Create a dictionary for tags_found and their corresponding percentages
tags_dict = dict(zip(tags_found, percentages))

# Map each label in assets_labels to its corresponding percentage in tags_dict
output = [tags_dict.get(label, '') for label in assets_labels]

print(output)

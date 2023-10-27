










import pdfplumber

pdf_path = '18_milestone\Rathbones\Rathbones PDFs\Core Strategy 2.pdf'

def extract_upper_assets_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[2]  # assuming you want to extract from the first page

        # PDF dimensions
        width = page.width
        height = page.height

        # Calculate the height for 22%
        desired_height = 0.22 * height

        # Crop to the desired area
        cropped = page.crop((0, 0, width, desired_height))

        # Extract text from the cropped area
        text = cropped.extract_text().split('\n')

    return text

def extract_lower_assets_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[2]  # assuming you want to extract from the first page

        # PDF dimensions
        width = page.width
        height = page.height

        # Cut by height
        top_height = 0.22 * height
        bottom_height = height - top_height

        # Cut by width
        left_width = 0.3425 * width
        right_width = width - left_width

        # Crop to the desired area
        cropped = page.crop((0, top_height, left_width, height))

        # Extract text from the cropped area
        text = cropped.extract_text().split('\n')

    return text

upper_assets_text = extract_upper_assets_from_pdf(pdf_path)
lower_assets_text = extract_lower_assets_from_pdf(pdf_path)



text = upper_assets_text + lower_assets_text
# print(upper_assets_text, lower_assets_text)

assets_labels = [
    'Equities',	
    'Conventional government bonds',
    'Government bonds (Overseas conventional)',
    'Government bonds (UK conventional)',	 
    'Alternative investment strategies',
    'Corporate bonds',	
    'Cash and equivalents',	
    'High quality credit (UK)',
    'High quality credit (Overseas)',
    'Commodities',
    'Infrastructure',
    'Private equity',
    'Equities (Overseas developed)',
    'Equities (UK)',
    'Equities (Asia/emerging markets)',
    'Corporate bonds (high yield)',	
    'Emerging market debt',
    'Specialist Credit',
    'Active managed fixed income',
    'Commodities',
    'Actively managed strategies',
    'Portfolio protection',
    'Property',
]

flattened_text = ' '.join(text)
    
asset_percentages = {}

for label in assets_labels:
    # Search for the label in the text
    index = flattened_text.find(label)
    
    if index != -1:
        # Move the index to the end of the label
        index += len(label)
        
        # Extract a substring from the current index and the next 10 characters (assuming max 10 chars for percentage value)
        substring = flattened_text[index:index+10]
        
        # Search for a percentage value in the substring
        percentage_start = substring.find(':')
        percentage_end = substring.find('%')

        # If both ':' and '%' are found, extract the percentage
        if percentage_start != -1 and percentage_end != -1:
            percentage = substring[percentage_start+1:percentage_end+1].strip()
            asset_percentages[label] = percentage
sorted_data = {k: v for k, v in sorted(asset_percentages.items(), key=lambda item: float(item[1][:-1]), reverse=True)}
print(sorted_data)
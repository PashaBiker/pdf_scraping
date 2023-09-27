import re
import pdf2image
from PIL import Image
import pytesseract


poppler_path = r'13_milestone\AJ\poppler-23.07.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path accordingly
# Convert PDF to images
pages = pdf2image.convert_from_path('13_milestone\AJ\MPS_Monthly_factsheets.pdf',
                                    dpi=300, first_page=2, last_page=5, poppler_path=poppler_path)

# Save the images temporarily (useful for debugging and OCR)
page_image_paths = []
for i, page in enumerate(pages, start=2):
    path = f"13_milestone\AJ\page_{i}.png"
    page.save(path, 'PNG')
    page_image_paths.append(path)


# Extract text from images using OCR
page_texts = []
for path in page_image_paths:
    text = pytesseract.image_to_string(Image.open(path))
    lines = [line for line in text.split('\n') if line.strip() != '']
    page_texts.append(lines)

print(page_texts)

data = page_texts


asset_labels = ['UK equity',
                'North America equity',
                'Europe ex-UK equity',
                'Asia Pacific ex-Japan equity',
                'Japan equity',
                'Emerging Markets equity',
                'UK government bonds ',
                'UK corporate bonds',
                'International bonds',
                'Property',
                'Cash equivalent',
                'Cash', ]

# 1. Extracting the filename
filename = [page[1] for i, page in enumerate(data) if i % 2 == 0]

# 2. Extracting the OCF value
OCF = []
for page in data:
    for line in page:
        if "OCF" in line:
            percentage = line.split()[-1]
            if "%" in percentage:
                OCF.append(percentage.replace('%',''))

# 3. Extracting the 1Y, 2Y, 3Y, 4Y, and 5Y values
values = []
for i, page in enumerate(data):
    if i % 2 != 0:  # even page
        for line in page:
            parts = [part for part in line.split() if '.' in part]
            if len(parts) > 3:  # checking if there are more than three values with dot
                values.append(parts)
                break

# Assuming values will always be in order
Y_values = {}
Y_values['1Y'] = [float(val[0]) for val in values]
Y_values['2Y'] = [float(val[1]) for val in values]
Y_values['3Y'] = [float(val[2]) for val in values]
Y_values['4Y'] = [float(val[3]) for val in values]
Y_values['5Y'] = [float(val[4]) for val in values]

# 4. Extracting the asset percentages based on the given asset labels
asset_labels = [
    'UK equity', 'North America equity', 'Europe ex-UK equity',
    'Asia Pacific ex-Japan equity', 'Japan equity', 'Emerging Markets equity',
    'UK government bonds ', 'UK corporate bonds', 'International bonds',
    'Property', 'Cash equivalent', 'Cash'
]

asset_percentages = []
pattern = re.compile(r'(\d+\.\d{2})%')  # Regular expression pattern to match percentages

for page in data:
    percentages_dict = {}
    for line in page:
        for label in asset_labels:
            if label in line:
                match = pattern.search(line)
                if match:
                    percent = match.group(1)
                    percentages_dict[label] = float(percent)
    asset_percentages.append(percentages_dict)

print("Filename:", filename)
print("OCF:", OCF)
print("Y values:", Y_values)
print("Asset percentages:", asset_percentages)
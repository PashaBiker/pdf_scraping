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

# print(page_texts)

data = page_texts
filename = []
OCF = []
performance_values = []

for i, page in enumerate(data):
    if i % 2 == 0:  # Odd pages
        filename.append(page[1])
        for line in page:
            if "OCF" in line:
                print(line)
                percentage = line.split()[-1]
                if "%" in percentage:
                    OCF.append(percentage.replace('%',''))
    else:  # Even pages
        float_values = [re.findall(r"[-]?\d+\.\d+", line) for line in page if len(re.findall(r"[-]?\d+\.\d+", line)) > 3]
        if float_values:
            # print(float_values)
            performance_values.append(float_values[2])

# Extracting 1Y, 2Y, 3Y, 4Y, 5Y values
# Assuming that the values are present in the 3rd line of the float values extracted
# This may need adjustment based on the actual data layout
if performance_values:
    year_values = performance_values[0]
    Y1, Y2, Y3, Y4, Y5 = year_values[0], year_values[1], year_values[2], year_values[3], year_values[4]

asset_labels = [
    'UK equity',
    'North America equity',
    'Europe ex-UK equity',
    'Asia Pacific ex-Japan equity',
    'Japan equity',
    'Emerging Markets equity',
    'UK government bonds',
    'UK corporate bonds',
    'International bonds',
    'Property',
    'Cash equivalent',
    'Cash'
]

asset_data = []

for page in data:
    assets = {}
    for line in page:
        for label in asset_labels:
            if label in line:
                # percentage value is before the label
                match = re.search(r"(\d+\.\d+)%", line)
                if match:
                    value = match.group(1)
                    assets[label] = float(value)
                else:
                    # Optionally: handle the case where the pattern isn't found
                    # (e.g., log a warning, set a default value, etc.)
                    pass
    if assets:
        asset_data.append(assets)

print("Filename:", filename)
print("OCF:", OCF)
print("1Y:", Y1, "2Y:", Y2, "3Y:", Y3, "4Y:", Y4, "5Y:", Y5)
print("Asset Data:", asset_data)
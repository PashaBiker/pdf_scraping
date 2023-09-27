import re
import pdf2image
from PIL import Image
import pytesseract
import os


# Initialize the paths and other constants
poppler_path = r'13_milestone\AJ\poppler-23.07.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
directory = "13_milestone\\AJ\\pictures\\"

def get_data(file):
    print("[INFO] Converting PDF to images...")
    pages = pdf2image.convert_from_path(file,
                                        dpi=300, first_page=2, last_page=9, poppler_path=poppler_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    page_image_paths = []
    for i, page in enumerate(pages, start=2):
        path = directory + f"page_{i}.png"
        page.save(path, 'PNG')
        page_image_paths.append(path)
        print(f"[INFO] Saved: {path}")

    print("[INFO] Extracting text from images using OCR...")
    page_texts = []
    def clean_text(lines, even_page):
        new_lines = []
        for line in lines:
            if even_page and '%' in line and 'OCF' not in line:
                line = re.sub(r'\b\d+(\.\d+)?%\b', '', line).strip()
            new_lines.append(line)
        return new_lines

    # Process each image path
    for index, path in enumerate(page_image_paths):
        print(f"[INFO] Processing image: {path}")
        text = pytesseract.image_to_string(Image.open(path))
        lines = [line.replace('J it','Japan equity').replace('Pacifi -','Pacific ex-') for line in text.split('\n') if line.strip() != '']
        # Check if page is even using its index
        even_page = (index + 1) % 2 == 0
        cleaned_lines = clean_text(lines, even_page)
        page_texts.append(cleaned_lines)

    data = page_texts

    print(data)

    print("[INFO] Extracting filename...")
    filename = [page[1] for i, page in enumerate(data) if i % 2 == 0]

    print("[INFO] Extracting OCF values...")
    OCF = []
    for page in data:
        for line in page:
            if "OCF" in line:
                percentage = line.split()[-1]
                if "%" in percentage:
                    OCF.append(percentage.replace('%',''))
                    print('[INFO] OCF appended:', percentage)

    print("[INFO] Extracting 1Y, 2Y, 3Y, 4Y, and 5Y values...")
    performance_values = []
    for i, page in enumerate(data):
        if i % 2 != 0:
            try:
                float_values = [re.findall(r"[-]?\d+\.\d+", line) for line in page if len(re.findall(r"[-]?\d+\.\d+", line)) > 3]
                if float_values:
                    performance_values.append(float_values[2])
                    print('[INFO] Performance values appended:', float_values[2])
            except:
                float_values = [re.findall(r"[-]?\d+\.\d+", line) for line in page if len(re.findall(r"[-]?\d+\.\d+", line)) >= 2]
                if float_values:
                    performance_values.append(float_values[2])
                    print('[INFO] Performance values appended (only 2 was):', float_values[2])

    Y1, Y2, Y3, Y4, Y5 = None, None, None, None, None

    if performance_values:
        year_values = performance_values[0]
        
        # Check and set values if they exist
        Y1 = year_values[0] if len(year_values) > 0 else Y1
        Y2 = year_values[1] if len(year_values) > 1 else Y2
        Y3 = year_values[2] if len(year_values) > 2 else Y3
        Y4 = year_values[3] if len(year_values) > 3 else Y4
        Y5 = year_values[4] if len(year_values) > 4 else Y5

    print("[INFO] Extracting asset percentages...")
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
                    match = re.search(r"(\d+\.\d+)%", line)
                    if match:
                        value = match.group(1)
                        assets[label] = float(value)
                        line = line.replace(match.group(0) + " " + label, '')
                    else:
                        pass
        if assets:
            asset_data.append(assets)
            print('[INFO] Asset data appended for this page')

    # print("[RESULTS] Filename:", filename)
    # print("[RESULTS] OCF:", OCF)
    # print("[RESULTS] Y values:", performance_values)
    # print("[RESULTS] Asset percentages:", asset_data)

    result2 = {}
    for i, name in enumerate(filename):  # assuming filename is a list of filenames
        Y1, Y2, Y3, Y4, Y5 = None, None, None, None, None

        year_values = performance_values[i]
        Y1 = year_values[0] if len(year_values) > 0 else Y1
        Y2 = year_values[1] if len(year_values) > 1 else Y2
        Y3 = year_values[2] if len(year_values) > 2 else Y3
        Y4 = year_values[3] if len(year_values) > 3 else Y4
        Y5 = year_values[4] if len(year_values) > 4 else Y5    
        result2[name] = {
            'OCF': OCF[i],
            '1Y': Y1,
            '2Y': Y2,
            '3Y': Y3,
            '4Y': Y4,
            '5Y': Y5,
            'Assets': asset_data[i]
        }
        print(
            'Filename', name, "\n",
            'OCF', OCF[i], "\n",
            '1Y', Y1, "\n",
            '2Y', Y2, "\n",
            '3Y', Y3, "\n",
            '4Y', Y4, "\n",
            '5Y', Y5, "\n",
            'Assets', asset_data[i], "\n",
        )
    return result2
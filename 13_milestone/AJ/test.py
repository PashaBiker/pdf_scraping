import pdf2image
from PIL import Image
import pytesseract


poppler_path = r'C:\Program Files\poppler-23.07.0\Library\bin'

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
    page_texts.append(text.strip().split('\n'))

print(page_texts)

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

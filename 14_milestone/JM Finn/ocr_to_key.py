import pytesseract
from PIL import Image

# Open the image file
img = Image.open("14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income Portfolio.pdf_page1_img1.png")
# Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(img)

print(text.split('/n'))

import easyocr
import numpy as np
from PIL import Image

# Open the image with PIL
img_pil = Image.open("14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income Portfolio.pdf_page1_img1.png")

# Convert the PIL Image object to a numpy array
img_np = np.array(img_pil)

# Create the EasyOCR reader
reader = easyocr.Reader(['en'])

# Read the text from the image numpy array
result = reader.readtext(img_np)
for entry in result:
    text = entry[1]
    print(text)
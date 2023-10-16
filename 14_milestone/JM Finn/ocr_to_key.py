from PIL import Image
import easyocr
import numpy as np

# Open the image file

img = '14_milestone\JM Finn\JM Images\key_image.png'
# img = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income and Growth Portfolio.pdf_page1_img4.png'
# img = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Growth Portfolio.pdf_page1_img4.png'

# Open the image with PIL
img_pil = Image.open(img)

# Convert the PIL Image object to a numpy array
img_np = np.array(img_pil)

# Create the EasyOCR reader
reader = easyocr.Reader(['en'])

assets = ['Fixed Income', 'UK Equities',
          'Intl. Equities', 'Property', 'Alternatives', 'Cash']

keys = []

# Read the text from the image numpy array
result = reader.readtext(img_np)
for entry in result:
    text = entry[1].replace('/', '').replace(':','.')
    keys.append(text)

print(keys)


def map_to_assets(input_list):
    # Initially set the result to an empty list
    result = []

    # Map items from input_list to corresponding assets
    for item in assets:
        # For 'Cap >' and 'Cap <', always add them regardless of their presence in input_list
        if item in ['Cap >', 'Cap <', 'Asia/China']:
            result.append(item)
        else:
            result.append(item if item in input_list else "")

    return result


output = map_to_assets(keys)

print(output)

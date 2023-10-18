import glob
import re
import fitz
import os
from PIL import Image
from io import BytesIO

import numpy as np
import easyocr

def is_within_range(resolution, target, px_range=10):
    width_check = target[0] - px_range <= resolution[0] <= target[0] + px_range
    height_check = target[1] - px_range <= resolution[1] <= target[1] + px_range
    return width_check and height_check

def pdf_image_extract(pdf_path, output_folder, pdf_name, page_num=None):
    allowed_resolutions = [(1018, 669), (1018, 556)]

    # Check if the output directory exists, if not create one
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_name = pdf_name.split('\\')[-1].replace('.pdf','')
    doc = fitz.open(pdf_path)
    extracted_images = []

    pages_to_process = [doc.load_page(page_num-1)] if page_num else [doc.load_page(i) for i in range(doc.page_count)]

    for page in pages_to_process:
        img_list = page.get_images(full=True)
        
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert image bytes to PIL Image for resolution check
            img_pil = Image.open(BytesIO(image_bytes))
            resolution = img_pil.size

            # Check if the resolution matches one of the allowed resolutions
            if any(is_within_range(resolution, allowed_res) for allowed_res in allowed_resolutions):
                # Construct the image path
                image_name = f"page_{page.number + 1}_img_{img_index + 1}_{pdf_name}.png"
                image_path = os.path.join(output_folder, image_name)

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                extracted_images.append(img_pil)

    print(f"Extracted images with the allowed resolutions are saved in {output_folder}")
    return extracted_images

def get_assets(pdf_path):
    extracted = pdf_image_extract(pdf_path=pdf_path, output_folder="16_milestone\FACET\Cropped images", pdf_name="assets_image", page_num=1)
    # TODO: CHANGE IMG TO PDF, 
    # Open the image using PIL
    img_pil = extracted[0]
    
    # Convert the PIL Image object to a numpy array
    img_np = np.array(img_pil)

    # Create the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    result = reader.readtext(img_np)

    keys = []

    # Extract only the percentages from the result
    for entry in result:
        text = entry[1].replace('/', '').replace(',', '.').replace('..', '.').replace('%', '').replace('|', '').strip()
        # print(text.split('\n'))

        # Extract all float numbers from the text
        numbers = re.findall(r"(\d+\.\d+|\d+)", text)

        # Add all valid numbers to keys
        for num in numbers:
            try:
                keys.append(float(num))
            except ValueError:
                pass

    # Create a dictionary by associating each asset with the respective percentage
    assets = ['Equities', 'Fixed Income', 'Property', 'Cash', 'Other']
    result_dict = {asset: keys[i*2] for i, asset in enumerate(assets)}

    # print(keys) # data from OCR
    # print(result_dict) # data from OCR + assets
    def truncate_number(num):
        s = str(num)
        if '.' in s:
            int_part, decimal_part = s.split('.')
            decimal_part = decimal_part[:2]  # Truncate without rounding
            return "{:.2f}".format(float(f"{int_part}.{decimal_part}"))
        return "{:.2f}".format(num)

    formatted_data = {k: truncate_number(v) for k, v in result_dict.items()}

    print(formatted_data) # output data
    return formatted_data

def crop_left_side(img, width=460):
    # No need to open the image again, just use the provided image
    
    # Crop 460px from the left
    left = 0
    upper = 0
    right = width
    lower = img.height
    cropped_img = img.crop((left, upper, right, lower))

    return cropped_img

def year_value(pdf_path):
    extracted = pdf_image_extract(pdf_path=pdf_path, output_folder="16_milestone\FACET\Cropped images", pdf_name="years_image", page_num=2)
    # Open the image using PIL
    img_pil = extracted[0]
    
    cropped_img = crop_left_side(img_pil)
    
    # Convert the PIL Image object to a numpy array
    img_np = np.array(cropped_img)

    # Create the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)


    result = reader.readtext(img_np)

    keys = []

    # Extract only the percentages from the result
    for entry in result:
        text = entry[1]
        # print(text)
        keys.append(text.split('\n'))
    flattened_list = [item[0] for item in keys]
    print(flattened_list)
    digits_only = [item for item in flattened_list if re.match(r'^-?\d+(\.\d+)?$', item)]
    print(digits_only)

    one_month = None
    if len(digits_only) > 0 and digits_only[0]:
        one_month = digits_only[0]
    one_year = None
    if len(digits_only) > 3 and digits_only[3]:
        one_year = digits_only[3]

    three_years = None
    if len(digits_only) > 4 and digits_only[4]:
        three_years = digits_only[4]

    five_years = None
    if len(digits_only) > 5 and digits_only[5]:
        five_years = digits_only[5]
    print('one month ',one_month)
    print('one year ',one_year)
    print('three years ',three_years)
    print('five years ',five_years)

    return one_month, one_year, three_years, five_years

if __name__ == "__main__":
    pdf_folder = '16_milestone\FACET\FACET PDFs/'
    output_folder = '16_milestone\FACET\images'
    pdfs = glob.glob(pdf_folder + '/*.pdf')

    

    # img_path = '16_milestone\FACET\images\page_2_img_2_Risk Level 9.png'
    img_path = '16_milestone\FACET\images\page_2_img_2_Passive Risk Level 4.png'
    output_image_path = '16_milestone\FACET\Cropped images'
    pdf_path = '16_milestone\FACET\FACET PDFs\Passive Risk Level 6.pdf'
    year_value(pdf_path)
    get_assets(pdf_path)
    
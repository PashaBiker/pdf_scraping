import glob
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

def pdf_image_extract(pdf_path, output_folder, allowed_resolutions, pdf_name):
    # Check if the output directory exists, if not create one
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    pdf_name = pdf_name.split('\\')[-1].replace('.pdf','')

    # Load the PDF with PyMuPDF
    doc = fitz.open(pdf_path)
    
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        
        # Get the images present in the page
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
                image_name = f"page_{page_number + 1}_img_{img_index + 1}_{pdf_name}.png"
                image_path = os.path.join(output_folder, image_name)
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

    print(f"Extracted images with the allowed resolutions are saved in {output_folder}")

if __name__ == "__main__":
    pdf_path = '16_milestone\FACET\FACET PDFs/'
    output_folder = '16_milestone\FACET\images'
    pdfs = glob.glob(pdf_path + '/*.pdf')
    allowed_resolutions = [(1018, 669), (1018, 556)]
    # for pdf in pdfs:
    #     pdf_image_extract(pdf, output_folder,allowed_resolutions,pdf)



    # img_pil = Image.open('16_milestone\FACET\images\page_1_img_6_Risk Level 2.png')

    # # Convert the PIL Image object to a numpy array
    # img_np = np.array(img_pil)
    path_pattern = '16_milestone/FACET/images/page_1*.png'

    # List to store all the numpy arrays of the images
    img_np_list = []

    # Loop through all matching files
    for img_path in glob.glob(path_pattern):
        # Open the image using PIL
        img_pil = Image.open(img_path)
        
        # Convert the PIL Image object to a numpy array
        img_np = np.array(img_pil)
        
        # Append the numpy array to the list
        img_np_list.append(img_np)

    # Create the EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    keys = []

    # Read the text from the image numpy array
    for image_p in img_np_list:
        # print(image_p)
        result = reader.readtext(image_p)
        for entry in result:
            text = entry[1].replace('/', '').replace(',', '.').replace('..','.')
            keys.append(text)

            print(text.split('\n'))
        print(keys)
        lines = keys
        result = {}

        # For every third line (assuming the structure is consistent), extract the asset class and percentage
        for i in range(0, len(lines), 3):
            asset_class = lines[i].strip()
            percentage = lines[i+1].strip('%').strip()  # Convert comma to dot and remove the percentage sign
            result[asset_class] = float(percentage)

        print(result)
            
    
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import easyocr
import pdfplumber
from fuzzywuzzy import process

def main(color, image_path):
    
    image = cv2.imread(image_path)
    threshold = 40

    # Create mask for the given color
    lower_bound = np.array(color) - threshold
    upper_bound = np.array(color) + threshold
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Apply mask to the image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('Cropped Image', result)
    # cv2.waitKey(0)


    MIN_CONTOUR_AREA = 500  # You can adjust this value
    output_data = []
    # Loop through the contours and crop the image based on bounding box of the contour
    for contour in contours:
        if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cropped_image = result[y:y+h, x:x+w]

        # Display cropped image
        # cv2.imshow('Cropped Image', cropped_image)
        # cv2.waitKey(0)

        gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        ocr_result = reader.readtext(cropped_image)
        
        extracted_text = ' '.join([item[1] for item in ocr_result])
        
        # Post-processing: Ensure only numbers remain
        # only_numbers = ''.join(filter(str.isdigit, extracted_text))
        output_text = extracted_text.replace(',','').strip()
        # print(output_text)
        output_data.append(output_text)
        output_data = [item for item in output_data if item != '']
    cv2.destroyAllWindows()
    return output_data


def extract_percentage_from_pdf(pdf_path):
    percentage_output = []

    with pdfplumber.open(pdf_path) as pdf:
        # Assuming you only want the second page's text
        page = pdf.pages[1]
        
        # Determine the new top boundary for cropping (50% of the page height)
        top_boundary = page.height * 0.5
        
        # Define the cropping box (bbox) as (x0, top, x1, bottom)
        cropped_page = page.crop(bbox=(0, top_boundary, page.width, page.height))
        
        # Extract text from the cropped area
        text = cropped_page.extract_text()
        # Split the text by spaces and check each word
        for word in text.split():
            if '%' in word:
                # Clean the word and append to the list
                cleaned_word = word.replace(',', '').replace(';', '').strip()
                percentage_output.append(cleaned_word)

    return percentage_output

def validation(data_text,output_data):
    # Threshold for similarity. This can be adjusted based on the desired sensitivity.
    THRESHOLD = 80

    matched_data = []

    for od in output_data:
        closest_match, score = process.extractOne(od, data_text)
        
        # If the similarity score meets or exceeds the threshold
        if score >= THRESHOLD:
            matched_data.append(closest_match)
            data_text.remove(closest_match)  # Remove the matched item so it doesn't get matched again

    # Now, append unmatched percentages from data_text to matched_data
    output_data = matched_data + data_text

    print(output_data)
    
    return output_data

if __name__ == "__main__":
    
    image_path = '12_milestone\Tideway Discretionary Fund Management Services\Screenshot_2.png'
    pdf_path = '12_milestone\Tideway Discretionary Fund Management Services\Multi-asset Moderate (DD2).pdf'

    data = {'Dated_Fixed_Income':(193,230,231),
            'Equity_Growth' : (88,194,173),
            'Equity_Income' : (247,148,30),
            'Alternatives': (0,174,239),
            'Fixed_Income' : (156,203,59)}
    
    # data = {'Dated_Fixed_Income':(193,230,231),
    #         'Fixed_Income' : (88,194,173),
    #         'Alternatives' : (247,148,30),
    #         'Equity_Income': (0,174,239),
    #         'Equity_Growth' : (156,203,59)}
    # print(data.items())
    percentages = extract_percentage_from_pdf(pdf_path)
    percentages.reverse()
    print(percentages)
    output_data = []
    for name, color in data.items():
        output_data.append(main(color, image_path))


    print(output_data)
    flattened_list = [item for sublist in output_data for item in sublist]
    print(flattened_list)
    result = validation(percentages, flattened_list)
    print(result)
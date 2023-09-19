import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import easyocr

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

    # Loop through the contours and crop the image based on bounding box of the contour
    for contour in contours:
        if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cropped_image = result[y:y+h, x:x+w]

        # Display cropped image
        cv2.imshow('Cropped Image', cropped_image)
        cv2.waitKey(0)

        gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        ocr_result = reader.readtext(cropped_image)
        
        extracted_text = ' '.join([item[1] for item in ocr_result])
        
        # Post-processing: Ensure only numbers remain
        # only_numbers = ''.join(filter(str.isdigit, extracted_text))
        print(extracted_text.replace(',','').strip())
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    image_path = '12_milestone\Tideway Discretionary Fund Management Services\Screenshot_16.png'
    data = {'Dated_Fixed_Income':(193,230,231),
            'Equity_Income': (0,174,239),
            'Alternatives' : (247,148,30),
            'Fixed_Income' : (88,194,173),
            'Equity_Growth' : (156,203,59)}

    for name, color in data.items():
        main(color, image_path)
import os
import re
import PyPDF2
import cv2
import matplotlib.pyplot as plt
import numpy as np
import easyocr
import pdfplumber
from fuzzywuzzy import process
from pdf2image import convert_from_path
from PIL import Image
import glob
import xlwings as xw
import requests
import traceback


def main():
# def main(color, image_path):
    image_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped assets\crop1_CSI Growth Portfolio.pdf_page1_img4.png'
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Define the color and threshold
    threshold = 21
    color = (174, 92, 55)

    # Create mask for the given color
    lower_bound = np.array(color) - threshold
    upper_bound = np.array(color) + threshold
    mask = cv2.inRange(image_rgb, lower_bound, upper_bound)

    # Apply mask to the image
    result = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

    # Display the masked image
    # plt.imshow(result)
    # plt.axis('off')
    # plt.title('Masked Image')
    # plt.show()

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('Cropped Image', result)
    cv2.waitKey(0)

    MIN_CONTOUR_AREA = 200  # You can adjust this value
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
        only_numbers = ''.join(filter(str.isdigit, extracted_text))
        output_text = extracted_text.replace(',', '').strip()
        print(output_text)
        output_data.append(output_text)
        output_data = [item for item in output_data if item != '']
        print(output_data)
    cv2.destroyAllWindows()
    return output_data


if __name__ == "__main__":
    main()
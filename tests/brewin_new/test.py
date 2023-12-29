


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
import pdfplumber
import fitz  # PyMuPDF

def extract_names_from_right_half(pdf_path, page_number=1):
    found_labels = []
    def create_asset_label_pattern(labels):
        # Escape special characters and join the labels into a single pattern
        escaped_labels = [re.escape(label) for label in labels]
        pattern = '|'.join(escaped_labels)
        return pattern

    # List of asset labels
    asset_labels = ['Bonds', 'Alternatives', 'Cash', 'Equities – UK', 'Equities – International']
    predefined_order = {label: i for i, label in enumerate(asset_labels)}
    asset_label_pattern = create_asset_label_pattern(asset_labels)
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) > page_number:
            page = pdf.pages[page_number]  # Select the desired page (1 for second page)

            # Define a clip region for the right half of the page
            width = page.width
            height = page.height
            bbox = (width / 2, 0, width, height)

            # Extract text from the defined area
            text = page.crop(bbox).extract_text()
            if text:
                # Regular expression to find percentages
                found_labels = re.findall(asset_label_pattern, text)

                # Sort the labels based on the predefined order
                sorted_labels = sorted(found_labels, key=lambda label: predefined_order.get(label, float('inf')))

    return sorted_labels

def get_voyager(pdf_path):
    def extract_text_blocks(pdf_path):

        doc = fitz.open(pdf_path)
        page = doc[1]  # assuming we are extracting from the first page

        text_blocks = page.get_text("blocks")
        indexed_blocks = {index: block for index, block in enumerate(text_blocks)}

        doc.close()
        return indexed_blocks
    
    def extract_text_blocks_from_right(pdf_path, page_number=1):
        doc = fitz.open(pdf_path)
        page = doc[page_number]  # Select the page (0-indexed)

        # Define a rectangular region for the right half of the page
        page_width = page.rect.width
        page_height = page.rect.height
        right_half_rect = fitz.Rect(page_width / 2, 0, page_width, page_height)

        # Extract text blocks from the defined region
        text_blocks = page.get_text("blocks", clip=right_half_rect)

        # Optionally, sort these blocks by their vertical position
        text_blocks.sort(key=lambda block: block[1])

        indexed_blocks = {index: block for index, block in enumerate(text_blocks)}

        doc.close()
        return indexed_blocks

    def extract_percentages(text_blocks):
        percentages = []
        for key, value in text_blocks.items():
            text = value[4]
            if "%" in text:
                lines = text.split('\n')
                for line in lines:
                    # Extract and convert each percentage value to float
                    percentage = line.strip().replace('%', '')
                    try:
                        percentages.append(float(percentage))
                    except ValueError as e:
                        # print(f"Error converting '{line}': {e}")
                        pass
        return percentages
    
    def extract_text_from_right_half(pdf_path):
        extracted_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[1]
            # Get the dimensions of the page
            width = page.width
            height = page.height

            # Define the bounding box for the right half
            # (x0, top, x1, bottom)
            bbox = (width / 2, 0, width, height)

            # Extract text from the defined area
            text = page.crop(bbox).extract_text()
            
            if text:
                extracted_text += text + "\n"
            percentages = re.findall(r'\d{1,2}\.\d+%', extracted_text)

        return percentages
    # Example usage

    percentages_from_text = extract_text_from_right_half(file_path)
    print(percentages_from_text)
    indexed_blocks = extract_text_blocks(file_path)

    # print(indexed_blocks)
    percentages = extract_percentages(indexed_blocks)
    print(percentages)
    # Convert list1 percentages to float

    list1_floats = [float(x.strip('%')) for x in percentages_from_text]

    # Define custom sorting key function
    def sort_key(x):
        try:
            return percentages.index(x)
        except ValueError:
            return float('inf')  # If not found, place at the end

    # Sort list1_floats based on their position in list2
    sorted_list1 = sorted(list1_floats, key=sort_key)

    # Convert back to strings with '%' if needed
    sorted_list1_str = [f'{x}%' for x in sorted_list1]


    asset_labels = extract_names_from_right_half(file_path)
    print(sorted_list1_str)
    print(asset_labels)
    portfolio = {label: percent.strip('%') for label, percent in zip(asset_labels, sorted_list1_str)}

    print(portfolio)
    return portfolio

if __name__ == "__main__":
    file_path = 'tests/brewin_new/Brewin Dolphin PDFs/MI RBC Brewin Dolphin Voyager – Max 80% Equity Class A.pdf'
    # extracted_images = extract_and_save_images_from_pdf(file_path, output_folder)
    s = get_voyager(file_path)
    print(s)
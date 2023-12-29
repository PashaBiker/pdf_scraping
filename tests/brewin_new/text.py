import re
import pdfplumber

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

# Replace 'your_pdf_file.pdf' with your PDF file path
pdf_path = 'tests/brewin_new/Brewin Dolphin PDFs/MI RBC Brewin Dolphin Voyager – Max 40% Equity Class A.pdf'
right_half_text = extract_text_from_right_half(pdf_path)
print(right_half_text)

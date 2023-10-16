


import re
import pdfplumber


pdf = '14_milestone\JM Finn\JM Finn PDFs\CSI Income Portfolio.pdf'

with pdfplumber.open(pdf) as pdf:
    # Get the second page from the PDF
    page = pdf.pages[1]

    # Calculate the page's width and height
    page_width = page.width
    page_height = page.height

    # Define a cropping rectangle for the left half of the page
    crop_rect = (0, 0, 0.5 * page_width, page_height)

    # Crop the page
    cropped_page = page.crop(bbox=crop_rect)

    # Extract the text from the cropped page and split by lines
    text_2_page = cropped_page.extract_text().split('\n')
    print(text_2_page)
    found_line = False

    for i, line in enumerate(text_2_page):
        percentage_matches = re.findall(r"\d+\.\d+%", line)
        
        if len(percentage_matches) > 3 and not found_line:
            years_matches = re.findall(r"(-?\d+\.\d+)", line)
            print(line)
            # Ensure there are at least 5 matches to avoid index errors
            if len(years_matches) >= 5:
                _1yr, _3yr, _5yr = years_matches[2], years_matches[3], years_matches[4]
                found_line = True
                

                print("1yr:", _1yr)
                print("3yr:", _3yr)
                print("5yr:", _5yr)
                break 
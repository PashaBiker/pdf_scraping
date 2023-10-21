

import glob
import re
import PyPDF2
from pdfminer.high_level import extract_text
import pdfplumber


def extract_left_text_from_page(page):
        # Calculate the x-coordinate which is 55% of the page width
        x_split = page.width * 0.54

        # Define the bounding box for the left 55%
        left_bbox = (0, 0, x_split, page.height)
        
        # Crop the page to the left 55% and extract text
        cropped_page = page.within_bbox(left_bbox)
        return cropped_page.extract_text()

def get_assets(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            asset_text = extract_left_text_from_page(pdf.pages[1])
            # print(asset_text.split('\n'))

        asset_labels = ['AsiaPac ex Japan Equity',
                        'Developed Equities (GBP hedged)',
                        'Liquidity',
                        'UK Equity',
                        'Japan Equity',
                        'Property',
                        'Global Equities',
                        'Europe ex UK Equity',
                        'Emerging Equity',
                        'Investment Grade Corporate Bonds (Global)',
                        'Global Government Bonds',
                        'US Equity',]  
        assets_result = {}
        # Convert the asset labels into a single regex pattern
        asset_labels_pattern = "|".join(map(re.escape, asset_labels))

        assets_result = {}
        for line in asset_text.split('\n'):
            match = re.search(asset_labels_pattern, line)
            if match:
                category = match.group(0)
                value_match = re.search(r'\b\d+(\.\d+)?', line[match.end():])
                if value_match:
                    value = value_match.group(0)
                    assets_result[category] = value

        print(assets_result)
        return assets_result

if __name__ == "__main__":
    pdf_folder = '17_milestone\HSBC Asset Management\HSBC Asset Management PDFs'
    # pdf_path ='17_milestone\HSBC Asset Management\HSBC Asset Management PDFs\Global Managed Portfolio Service Adventurous Portfolio.pdf'
    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf in pdfs:


        def get_data(pdf):
            extracted_text_1_page = extract_text(pdf, maxpages=1)
            text = extracted_text_1_page.split('\n')
            for i,line in enumerate(text):
                if 'Ongoing charge figure' in line:
                    OCF = text[i+1].replace('%', '')
                    # print(OCF)

            with pdfplumber.open(pdf) as pdf:
                text = pdf.pages[1].extract_text()
                text = text.split('\n')
                    
                for i, line in enumerate(text):
                    if "6 month" in line:
                        years_string = text[i+1]
                        values = re.findall(r'-?\d+\.\d+', years_string)
                        one_month = values[1]
                        one_year = values[4]
                        three_years = values[5]
                        five_years = values[6]
                        data_string = text[1]
                        split_parts = re.split(r'(\d{2} \w+ \d{4})', data_string)
                        date = split_parts[1]
                        print(date)
                        # print(f"One Month: {one_month}")
                        # print(f"One Year: {one_year}")
                        # print(f"Three Years: {three_years}")
                        # print(f"Five Years: {five_years}")
            return date, OCF, one_month,one_year,three_years,five_years
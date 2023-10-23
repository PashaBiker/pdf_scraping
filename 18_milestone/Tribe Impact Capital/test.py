
















import re
import pdfplumber

pdf = '18_milestone\Quilter\Quilter PDFs\WealthSelect Managed Active 7.pdf'

def get_data(pdf):

    with pdfplumber.open(pdf) as pdf:
        first_page_text = pdf.pages[0].extract_text()
        first_page_text = first_page_text.split('\n')
        print(first_page_text)

        first_page = pdf.pages[0] 

        # Define the cropping area based on the page's width and height
        first_page_crop_width_start = first_page.width * 0.5
        first_page_crop_width_end = first_page.width
        first_page_crop_height = first_page.height * 0.5

        crop_box = (first_page_crop_width_start, 0, first_page_crop_width_end, first_page_crop_height)  # (x0, y0, x1, y1)

        # Crop the page
        right_part_cropped_page = first_page.crop(bbox=crop_box)

        # Extract text from the cropped area
        right_part_text = right_part_cropped_page.extract_text().split('\n')
        print(right_part_text)

        for i, line in enumerate(right_part_text):
            if 'Weighted fund charge' in line:
                charge_values_line = right_part_text[i+1]
                charge_values = re.findall(r'\d+\.\d+', charge_values_line)
                # print(charge_values)
                weighted_charge = charge_values[0]
                mps_charge = charge_values[1]
                print(weighted_charge, ' weighted_charge')
                print(mps_charge, ' mps_charge')

        for i, line in enumerate(first_page_text):
            if 'as at' in line:
                date_line = re.search(r'as at ((?:\S+\s?){3})', line)
                date = date_line.group(1).strip()
                print(date)

            if '3 years' in line:
                numbers_line = first_page_text[i + 1]
                
                # Check if the line contains any float values. If not, get the next line.
                if not re.search(r'\d+\.\d+', numbers_line):
                    numbers_line = first_page_text[i + 2]

                numbers = re.findall(r'-?\d+\.\d+|-', numbers_line)
                print("Extracted numbers:", numbers)  # Debugging information

                # Convert numbers to float or None if '-'
                numbers = [float(num) if num != '-' else None for num in numbers]

                # Extract the specific values you're interested in using safe_get
                one_year = safe_get(numbers, 1)
                three_years = safe_get(numbers, 2)
                five_years = safe_get(numbers, 3)

                print(one_year,' 1y')
                print(three_years,' 3y')
                print(five_years,' 5y')

        third_page = pdf.pages[2]  # Remember that the index is 0-based

        # Define the cropping area based on the page's width and height
        crop_width = third_page.width * 0.5
        crop_height = third_page.height * 0.5

        crop_box = (0, 0, crop_width, crop_height)  # (x0, y0, x1, y1)

        # Crop the page
        cropped_page = third_page.crop(bbox=crop_box)

        # Extract text from the cropped area
        asset_text = cropped_page.extract_text().split('\n')
        # print(asset_text)

        asset_labels = [
            'Developed markets (ex UK) equity',
            'Emerging markets equity',
            'UK equity',
            'Fixed interest',
            'Cash',
            'Emerging markets multi-thematic equity',
            'Engagement equity',
            'Global multi-thematic equity',
            'Social equity',
            'Environmental equity',
            'Alternatives',]
        
        asset_labels_pattern = "|".join(map(re.escape, asset_labels))

        assets_result = {}
        for line in asset_text:
            match = re.search(asset_labels_pattern, line)
            if match:
                category = match.group(0)
                value_match = re.search(r'\b\d+(\.\d+)?', line[match.end():])
                if value_match:
                    value = value_match.group(0)
                    assets_result[category] = value

        # print(assets_result)  
    # return date, one_year, three_years, five_years, weighted_charge, mps_charge, date
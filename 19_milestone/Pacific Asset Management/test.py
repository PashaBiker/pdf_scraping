import glob
import re
import pdfplumber
from datetime import datetime
# Path to your PDF file
pdf_path = '19_milestone\Pacific Asset Management\Pacific Asset Management PDFs\Sustainable Conservative.pdf'

# Open the PDF file
def get_one_year(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            # Calculate the crop dimensions (53.2% of the page width)
            width = page.width
            height = page.height
            left_crop_percentage = 0.532
            left_crop_width = width * left_crop_percentage

            # Define the box (x0, top, x1, bottom) to crop - we start from the top-left corner
            crop_box = (0, 0, left_crop_width, height)

            # Crop the page
            cropped_page = page.within_bbox(crop_box)

            # Extract text from the cropped page
            text = cropped_page.extract_text()

            lines = text.split('\n')

            # Pattern to match the line of interest
            counter = 0  # Инициализируем счетчик найденных строк
            for line in lines:
                match = re.search(r'Portfolio.*%.*%.*%.*%.*%', line)
                if match:
                    counter += 1  # Увеличиваем счетчик, если нашли совпадение
                    if counter == 2:  # Проверяем, второе ли это совпадение
                        year_line = match.group(0)  # Извлекаем строку совпадения
                        # print(year_line)
                        numbers = re.findall(r'-?\d+\.\d+', year_line)
                        one_year = numbers[-1] if numbers else None
                        print(one_year)
    return one_year



def find_lines_with_multiple_percentages(text_list, min_percentages=4):
    # Regular expression to match percentage values
    percentage_pattern = re.compile(r'(-?\d+(\.\d+)?%)')

    # Function to check for the minimum occurrences of percentage pattern
    def min_percentage_occurrences(line, min_count):
        # Skip the line if 'Mar' is found in it.
        if 'Mar' in line or 'Jun' in line:
            return False
        return len(percentage_pattern.findall(line)) >= min_count

    # Search each line for the pattern and return lines that match the criterion
    return [line for line in text_list if min_percentage_occurrences(line, min_percentages)]


def get_data(pdf_path):
    
    def reformat_date(date_str):
        # Remove 'AS AT ' prefix
        date_str = date_str.replace('AS AT ', '')

        # Parse the date string to a datetime object
        date_obj = datetime.strptime(date_str, '%d %b %Y')

        # Format the datetime object to the desired format (e.g., "31 August 2023")
        normal_date = date_obj.strftime('%d %B %Y')

        return normal_date
    
    lines = [] 

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from the current page
            text = page.extract_text()
            if text:  # Checking if text was extracted
                # Split text into lines and extend the all_lines list
                lines.extend(text.split('\n'))
    # print(lines)
    matching_lines = find_lines_with_multiple_percentages(lines)

    charges_line = matching_lines[0]
    # print(matching_lines)
    percentages = charges_line.split()

    # Assign the first and third percentage values to DFM and OCF
    DFM = percentages[0]  # The first percentage
    OCF = percentages[2]

    for line in lines:
        if "AS AT" in line:
            # print(line)
            date = reformat_date(line)

    return date, OCF, DFM

def get_assets_groups_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Initialize a list to collect text
        text_lines = []

        for page in pdf.pages:
            width = page.width
            height = page.height
            left_crop_percentage = 0.203
            left_crop_width = width * left_crop_percentage

            # Define the box (x0, top, x1, bottom) to crop - we start from the top-left corner
            crop_box = (0, 0, left_crop_width, height)

            # Crop the page
            cropped_page = page.within_bbox(crop_box)

            # Extract text from the cropped page
            extracted_text = cropped_page.extract_text()
            
            if extracted_text:  # Checking if text was extracted
                # Split the text by new lines and extend the list
                text_lines.extend(extracted_text.split('\n'))

        # print(text_lines)
        # Find the starting and ending indices
        start_index = next((i for i, line in enumerate(text_lines) if 'Asset Class' in line), None)

        # Find the end index, starting the search from the start_index
        end_index = next((i for i, line in enumerate(text_lines[start_index:]) if 'Source' in line), None)

        # If we found an end_index, we need to offset it by the start_index because the search was on a sliced list
        if end_index is not None and start_index is not None:
            end_index += start_index

        # Now you can extract the lines between these indices
        if start_index is not None and end_index is not None:
            asset_class_lines = text_lines[start_index:end_index]
        else:
            asset_class_lines = []
        
        grouped_asset_labels = [
                        'Equity',
                        'Fixed Income',
                        'Alternatives',
                        'Diversifying Assets',
                        'Absolute Return',
                        'Cash',]
        
        # print(extracted_lines)
        # Initialize a dictionary to hold the asset percentages
        asset_percentages = {label: None for label in grouped_asset_labels}

        # Process the extracted lines and populate the asset_percentages dictionary
        # Process each line to find labels and their corresponding percentages
        for i, line in enumerate(asset_class_lines):
            # Split line into label and percentage if possible
            parts = line.split(':')
            if len(parts) == 2 and parts[1].strip():  # Label and percentage on the same line
                label, percentage_str = parts[0], parts[1]
                if label in asset_percentages:
                    # Clean and convert the percentage to a float
                    percentage = float(percentage_str.replace('%', '').strip())
                    asset_percentages[label] = percentage
            elif len(parts) == 1 or (len(parts) == 2 and not parts[1].strip()):
                # Handle case where the percentage is on the next line
                label = parts[0].strip()
                if label in asset_percentages and i + 1 < len(asset_class_lines):
                    next_line = asset_class_lines[i + 1]
                    if next_line.strip().endswith('%'):
                        percentage = float(next_line.replace('%', '').strip())
                        asset_percentages[label] = percentage


        # print(asset_class_lines)
        print(asset_percentages)
        total = sum(value for value in asset_percentages.values() if value is not None)

        # print('\n',"The sum of the investment portfolio is:", total , '\n')
    return asset_percentages

def get_assets(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract tables from the page
            tables = page.extract_tables()
            # Check each table
                    
            asset_labels = [
                            'Global Equity',
                            'UK Equity',
                            'US Equity',
                            'Emerging Equity',
                            'Japan Equity',
                            'Europe Equity',
                            'UK Government Bonds',
                            'Investment Grade Corporate Bonds (Global)',
                            'Global Bonds',
                            'Investment Grade Corporate Bonds (Ultrashort)',
                            'Investment Grade Corporate Bonds (GBP)',
                            'EM Bonds',
                            'REITS',
                            'Absolute Return',
                            'Diversifying Risk Assets',
                            'Cash',
                            
                            
                            'Strategic Fixed Income',
                            'Specialist Fixed Income',
                            'AsiaPac ex Japan Equity',
                            'Investment Grade Corporate Bonds',
                            'Thematic Equity',
                            'Europe ex UK Equity',]
            for table in tables:
                # Check if 'Asset Class' is in any of the table headers
                for row in table:
                    if 'Asset Class' in row:
                        # Found the table with 'Asset Class'
                        for sublist in table:
                            for i, item in enumerate(sublist):
                                if isinstance(item, str):  # Check if the item is a string
                                    sublist[i] = item.replace('\n', ' ')

                        asset_class_table = table
                        # Now process this table as required
                        # For example, print it or extract data from it
                        # print(asset_class_table)
                        # Initialize a dictionary to hold the sum of percentages for each asset label
                        label_percentages = {label: None for label in asset_labels}

                        # Variable to keep track of the current label
                        current_label = None

                        # Iterate through the asset data
                        for row in asset_class_table:
                            # Skip the header row
                            if row[0] == 'Asset Class':
                                continue

                            # Check if a new label is provided (not None and not empty after stripping whitespace)
                            if row[1] is not None and row[1].strip():
                                current_label = row[1].strip()

                            # Make sure we're dealing with an asset label we recognize
                            if current_label not in label_percentages or label_percentages[current_label] is None:
                                label_percentages[current_label] = 0

                            # Now you can safely add the float value
                            label_percentages[current_label] += float(row[4])

                        print(label_percentages)
                        total = sum(value for value in label_percentages.values() if value is not None)

                        # print('\n',"The sum of the investment portfolio is:", total , '\n')

    return label_percentages

def sum_assets(assets_part, assets_groups):
    combined_assets = {}

    # Sum values from assets_part
    for key, value in assets_part.items():
        if value is not None:
            combined_assets[key] = value

    # Sum values from assets_groups
    for key, value in assets_groups.items():
        if key in combined_assets and combined_assets[key] is not None:
            # If both values are numbers, sum them
            if value is not None:
                combined_assets[key] += value
        else:
            # If the key doesn't exist in combined_assets or its value is None, add/overwrite it
            combined_assets[key] = value

    return combined_assets

if __name__ == "__main__":
    pdf_folder = '19_milestone\Pacific Asset Management\Pacific Asset Management PDFs'

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    for pdf_path in pdfs:
        # print(pdf_path)
        one_year = get_one_year(pdf_path)
        assets_part = get_assets(pdf_path)
        assets_groups = get_assets_groups_text(pdf_path)
        assets = sum_assets(assets_part, assets_groups)

        date, OCF, DFM = get_data(pdf_path)
        print(date, OCF, DFM)
        print(assets)
    
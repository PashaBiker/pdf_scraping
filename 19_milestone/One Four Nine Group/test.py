import re
import pdfplumber   







pdf_path = '19_milestone\One Four Nine Group\One Four Nine Group PDFs\Active Defensive Model.pdf'

def get_data(pdf_path):
    def safe_get(lst, index, default=None):
            return lst[index] if index < len(lst) else default

    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        first_page_text = first_page.extract_text().split('\n')
        second_page = pdf.pages[1]
        
        # Get the page's width and height
        width = second_page.width
        height = second_page.height
        
        # Calculate x1 for 59.375% of the page width
        x1 = 0.59375 * width
        
        # Define bounding box
        bbox = (0, 0, x1, height)
        
        # Crop the page
        cropped_page = second_page.crop(bbox)
        
        # Extract text from the cropped page
        second_page_text = cropped_page.extract_text().split('\n')

        # print(text)
        print(second_page_text)
        for i,line in enumerate(first_page_text):
            if 'One Four Nine Fee' in line:
                # print(line)
                OFN_fee = re.findall(r'\d.\d\d', line)[0]
                print(OFN_fee, 'ofn fee')
            if 'Underlying Fund Fees' in line:
                # print(line)
                UF_fee = re.findall(r'\d.\d\d', line)[0]
                print(UF_fee, 'uf fee')

            if '3 Years' in line:
                numbers_line = first_page_text[i + 1]
                
                # Check if the line contains any float values. If not, get the next line.
                if not re.search(r'\d+\.\d+', numbers_line):
                    numbers_line = first_page_text[i + 2]

                numbers = re.findall(r'-?\d+\.\d+|N/A|-', numbers_line)
                print("Extracted numbers:", numbers)  # Debugging information

                # Convert numbers to float or None if 'N/A'
                numbers = [float(num) if num != 'N/A' else None for num in numbers]

                # Extract the specific values you're interested in using safe_get
                one_month = safe_get(numbers, 0)
                one_year = safe_get(numbers, 2)
                three_years = safe_get(numbers, 3)

                print(one_month,' 1m')
                print(one_year,' 1y')
                print(three_years,' 3y')

            if 'as at' in line:
                date_line = line.split('as at ')
                date = date_line[-1]
                # print(date)

        # for i,line in enumerate(second_page_text):
        #     for line in second_page_text:
        #         print()

        asset_labels_pattern = [
            'Cash',
            'UK Gilts'	,
            'International Sovereign Bonds'	,
            'Investment Grade Corporate Bonds'	,
            'High Yield Bonds'	,
            'UK Equity'	,
            'US Equity'	,
            'Japan Equity'	,
            'Europe ex UK Equity'	,
            'Asia Pacific ex Japan Equity'	,
            'Global Emerging Equity',
            'Gold',
        ]
        asset_labels = sorted(asset_labels_pattern, key=lambda x: len(x), reverse=True)
        asset_allocation = {}

        for i, line in enumerate(second_page_text):
            # Check if a line contains a percentage value
            if "(" in line and "%" in line:
                percentage = line.split('(')[-1].split(')')[0]
                
                # Check the current line for labels
                asset_label_found = False
                for label in asset_labels:
                    if label in line:
                        asset_allocation[label] = percentage
                        asset_label_found = True
                        break
                
                # If no label is found in the current line, check the previous line
                if not asset_label_found:
                    # Get combined labels from multiple lines
                    combined_previous = second_page_text[i-1]
                    combined_current = " ".join(line.split(' ')[:-1])  # Excluding the last word which contains the percentage
                    combined_label = combined_previous + " " + combined_current

                    for label in asset_labels:
                        if label in combined_label:
                            asset_allocation[label] = percentage
                            break

        print(asset_allocation)

    return date, OFN_fee, UF_fee, one_month, one_year, three_years, asset_allocation


if __name__ == '__main__':
    get_data(pdf_path)
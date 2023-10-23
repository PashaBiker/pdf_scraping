
















import re
import pdfplumber

pdf_path = '18_milestone\Tribe Impact Capital\Tribe Impact Capital PDFs\Medium-low risk.pdf'



def get_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        text = text.split('\n')

        for line in text:
            if 'AS AT' in line:
                date_parts = line.split('AS AT: ')
                date = date_parts[1].replace('/','.') if len(date_parts) > 1 else None
                # print(date)
            if 'MANAGEMENT FEE' in line:
                management_fee = re.search(r'(\d+\.\d+)', line).group(1)
                # print(management_fee)
                
            if 'OCF OF UNDERLYING FUNDS' in line:
                OCF = re.search(r'(\d+\.\d+)', line).group(1)
                # print(OCF)

        second_page = pdf.pages[1]
        text = second_page.extract_text()
        asset_text = text.split('\n')
        print(asset_text)

        
        asset_labels = ['CASH',	
                        'GOVERNMENT BOND',	
                        'INVESTMENT GRADE',	
                        'UK EQUITY',	
                        'GLOBAL EQUITY',	
                        'ASIA PACIFIC EQUITY',	
                        'EMERGING MARKETS',]

        asset_labels_pattern = "|".join(map(re.escape, asset_labels))

        assets_result = {}

        # Regular expression pattern to match percentages followed by asset labels
        pattern = r'(\d+\.?\d*)%\s*(' + asset_labels_pattern + r')'

        # Debug: Print the pattern
        # print("Pattern:", pattern)

        # Searching for matches in each line of asset_text
        for line in asset_text:
            match = re.search(pattern, line)
            if match:
                # Debug: Print the matched line
                # print("Matched Line:", line)
                # If a match is found, update the assets_result dictionary
                assets_result[match.group(2)] = float(match.group(1))

        print(assets_result)

        def extract_one_year(pdf_path):
            with pdfplumber.open(pdf_path) as pdf:
                first_page = pdf.pages[0]
                tables = first_page.extract_tables()

                # for i, table in enumerate(tables):
                    # print(f"Table {i + 1}:")
                    # for row in table:
                        # print(row)
                    # print("-" * 40)

                # Extract the desired value from the third table (index 2)
                one_year = tables[2][2][-1].replace('%','')
                print(f"one_year Value: {one_year}")

        one_year = extract_one_year(pdf_path)


    return OCF, management_fee, one_year ,assets_result,date


import re

text = "The SIMPS Portfolio range PORTFOLIO FACTS AS AT: 30/09/2023 all over the world. There are fears that the US"

pattern = r'AS AT:\s*([\d/]+)'
match = re.search(pattern, text)
if match:
    date_after_as_at = match.group(1).replace('/','.')
    print("Date after 'AS AT:':", date_after_as_at)
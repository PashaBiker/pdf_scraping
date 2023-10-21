






import re
import pdfplumber


pdf = '17_milestone\Parmenion\Parmenion PDFs\PIM Strategic Ethical Active A RG6.pdf'

with pdfplumber.open(pdf) as pdf:
    first_page_text = pdf.pages[0].extract_text()
    second_page_text = pdf.pages[1].extract_text()
    first_page_text = first_page_text.split('\n')
    second_page_text = second_page_text.split('\n')

    print(first_page_text)
    # breakpoint()
    print(second_page_text)

    asset_labels = ['Managed Liquidity',
        	        'Global Government Bonds',	
                    'Global Index-Linked Government Bonds',	
                    'Sterling Corporate Bonds',	
                    'Global Bonds',	
                    'Diversified Alternatives',	
                    'UK Equity Income',	
                    'UK Equity',	
                    'US Equity',	
                    'Europe ex UK Equity	Japan Equity',	
                    'Asia Pacific ex Japan Equity',	
                    'Emerging Markets Equity	Managed Liquidity (Unscreened)',	
                    'UK Gilts',	
                    'International Equity',	
                    'Emerging Markets / Asia Pacific ex Japan Equity',]  
    assets_result = {}
    # Convert the asset labels into a single regex pattern
    asset_labels_pattern = "|".join(map(re.escape, asset_labels))
    # Identify the start and end indices
    for idx, line in enumerate(second_page_text):
        if 'Asset Allocation' in line:
            start_index = idx
        if 'Fund Allocation' in line:
            end_index = idx
    assets_result = {}
    for line in second_page_text[start_index + 1:end_index]:
        match = re.search(asset_labels_pattern, line)
        if match:
            category = match.group(0)
            value_match = re.search(r'\b\d+(\.\d+)?', line[match.end():])
            if value_match:
                value = value_match.group(0)
                assets_result[category] = value

    print(assets_result)
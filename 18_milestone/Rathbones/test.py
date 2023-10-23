










import pdfplumber

pdf_path = '18_milestone\Rathbones\Rathbones PDFs\Core Strategy 2.pdf'

with pdfplumber.open(pdf_path) as pdf:
    extracted_text = ''
    
    # # Iterate from page 2 to 13 (remember that in Python, indexing is 0-based)
    # for i in range(1, 13): 
    #     page = pdf.pages[i]
    #     extracted_text += page.extract_text()

    page = pdf.pages[2]
    
    extract_tables = page.extract_text().split('\n')
    print(extract_tables)

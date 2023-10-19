

import PyPDF2
from pdfminer.high_level import extract_text


if __name__ == "__main__":
    pdf_path ='17_milestone\HSBC Asset Management\HSBC Asset Management PDFs\Global Managed Portfolio Service Adventurous Portfolio.pdf'
    extracted_text = extract_text(pdf_path)
    print(extracted_text.split('\n'))
import PyPDF2
import re

# def extract_percentages_from_pdf(pdf_path):
#     # Open the PDF file
#     with open(pdf_path, 'rb') as file:
#         # Initialize PDF reader
#         pdf_reader = PyPDF2.PdfReader(file)


#         # Extract text from the second page
#         page_text = pdf_reader.pages[1].extract_text()

#         # Use regex to find all percentages in the text
#         percentages = re.findall(r'(\d+\.\d+)%', page_text)

#         # Convert the percentages to floats for sorting
#         percentages_float = [float(p) for p in percentages]

#         # Sort the percentages
#         sorted_percentages = sorted(percentages_float, reverse=True)

#         # Convert back to string with '%' appended
#         sorted_percentages_str = [f"{p}%" for p in sorted_percentages]

#         return sorted_percentages_str

# # Path to the PDF (replace with the path to your downloaded PDF)
# pdf_path = '12_milestone/Tideway Discretionary Fund Management Services/222.pdf'
# sorted_percentages = extract_percentages_from_pdf(pdf_path)
# print(sorted_percentages)


import PyPDF2
import re


def extract_bottom_half_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page_text = pdf_reader.pages[1].extract_text()
        lines = page_text.split('\n')
        half_index = len(lines) // 2
        return '\n'.join(lines[half_index:])


def extract_and_sort_percentages(text):
    # Extract all percentages from the text
    percentages = re.findall(r'(\d+\.\d+)%', text)
    return percentages


pdf_path = '12_milestone/Tideway Discretionary Fund Management Services/222.pdf'
# bottom_half_text = extract_bottom_half_from_pdf(pdf_path)
bottom_half_text = """
Alternatives
'Equity Income 6.25%'
'Equity Growth32.18%'
'22.83%18.75%'
'20.00%
                 """
sorted_percentages = extract_and_sort_percentages(bottom_half_text)
print(sorted_percentages)

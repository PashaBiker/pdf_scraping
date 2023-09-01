# import PyPDF2

# file = 'Multi-asset Moderate (DD2).pdf'

# with open(file, 'rb') as pdf_file:
#     reader = PyPDF2.PdfReader(pdf_file)
#     page = reader.pages[1]  # извлекаем текст только со второй страницы
#     text = page.extract_text().split("\n")

# print(text)

# from pdfminer.high_level import extract_text

# file = 'Multi-asset Moderate (DD2).pdf'

# # Этот метод извлекает текст из всего документа
# full_text = extract_text(file)
# text_by_pages = full_text.split("\x0c")  # разделение по страницам
# text = text_by_pages[1].split("\n")  # извлекаем текст только со второй страницы

# print(text)

import slate3k as slate

file = 'Multi-asset Moderate (DD2).pdf'

with open(file, 'rb') as pdf_file:
    extracted_text = slate.PDF(pdf_file)
text = extracted_text[1].split("\n")

print(text)
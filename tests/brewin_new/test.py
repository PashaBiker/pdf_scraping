





import pdfplumber



file_path = 'tests/brewin_new/Brewin Dolphin PDFs/MI RBC Brewin Dolphin Voyager – Max 90% Equity Class A.pdf'

# # Открытие PDF файла и чтение текста с правой части второй страницы
# with pdfplumber.open(file_path) as pdf:
#     # Получение второй страницы
#     page = pdf.pages[1]

#     # Определение размеров страницы
#     width = page.width
#     height = page.height

#     # Выделение правой половины страницы
#     right_half = page.crop((width / 2, 0, width, height))

#     # Извлечение текста с правой половины страницы
#     extracted_text = right_half.extract_text()

#     print(extracted_text)

from PyPDF2 import PdfReader

# Открытие и чтение PDF файла с использованием PyPDF2
reader = PdfReader(file_path)
page = reader.pages[1]

# Получение текста со второй страницы
full_text = page.extract_text()

# Вычисление координат для правой части страницы
# Примечание: PyPDF2 не позволяет напрямую обрезать страницу, так что мы разделим текст по словам и выберем те, которые предположительно находятся справа
words = full_text.split()
print(words)
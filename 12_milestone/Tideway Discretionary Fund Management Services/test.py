import tika
tika.initVM()
from tika import parser
import os
import traceback
import requests
import xlwings as xw
import pdfplumber
from PyPDF2 import PdfReader
import re
import glob
from pdfminer.high_level import extract_text
import fitz

text = ""

file = "12_milestone/Tideway Discretionary Fund Management Services/222.pdf"
# file = '12_milestone\Tideway Discretionary Fund Management Services\Multi-asset Moderate (DD2).pdf'

# doc = fitz.open(file)
# for page in doc:
#     text += page.get_text()

# text = text.split("\n")
# print(text)

# import PyPDF2

# with open(file, 'rb') as file:
#     reader = PyPDF2.PdfReader(file)
#     text = ""
#     for page in range(len(reader.pages)):
#         text += reader.pages[page].extract_text()
#     text = text.split("\n")
# print(text)

# from pdfminer.high_level import extract_text

# text = extract_text(file)

# text = text.split("\n")
# print(text)
import slate3k as slate
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

def pdf_to_text(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        return output_string.getvalue()

file_path = file
extracted_text = pdf_to_text(file_path)
text = extracted_text.split("\n")
print(text)

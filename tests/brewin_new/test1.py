import pdfplumber

def extract_tables_from_pdf(pdf_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Iterate through each page in the PDF
        for page in pdf.pages:
            # Extract tables from the current page
            tables = page.extract_tables()

            # Process each table
            for table in tables:
                # Check if the table has more than two rows and more than five columns
                if len(table) > 2 and all(len(row) > 5 for row in table):
                    print("Table found on page:", page.page_number)
                    print(table)


# Example usage
pdf_path = 'tests/brewin_new/Brewin Dolphin PDFs/MI RBC Brewin Dolphin Voyager – Max 70% Equity Class A.pdf'
extract_tables_from_pdf(pdf_path)

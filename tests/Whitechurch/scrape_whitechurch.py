import requests
from bs4 import BeautifulSoup
import xlwings as xw
import traceback


def scrape_links(file_urls):
    pdf_links = {}

    for key, url in file_urls.items():
        if key in pdf_links:
            print("PDF link of " + key + " already exists.")
            continue

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all('a')

        for link in links:
            if link.text.strip().replace('>', '') == key.strip():
                pdf_links[key.strip()] = 'https://www.whitechurch.co.uk' + \
                    link['href']
                print("Found PDF link of " + key)
                break

    # for key, value in pdf_links.items():
    #     print(key + ": " + value)

    return pdf_links


def get_urls(spreadsheet):
    print('Getting URLs from spreadsheet...')
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets['PDF Scraping']

        pdf_url_range = sheet.range('B2').expand('down').value
        pdf_name_range = sheet.range('C2').expand('down').value

        file_urls = dict(zip(pdf_name_range, pdf_url_range))

        return file_urls

    except Exception as e:
        traceback.print_exc()

    finally:
        wb.save()
        wb.close()


def write_to_sheet(pdf_link, spreadsheet):
    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)
        sheet = wb.sheets["PDF Scraping"]

        range_values = sheet.range("C1").expand("down").value

        for i, row in enumerate(range_values):
            for key, value in pdf_link.items():
                if row != None and row.strip() == key.strip():
                    cell = sheet.range("D" + str(i + 1))
                    cell.value = value
                    print("Writing PDF link of " + key + "...")
                    break

    except Exception as e:
        traceback.print_exc()

    finally:
        wb.save()
        wb.close()


if __name__ == "__main__":
    # enter the name of the excel file
    excel_file = "tests\Whitechurch\Whitechurch Securities Ltd.xlsm"

    file_urls = get_urls(excel_file)
    pdf_link = scrape_links(file_urls)
    write_to_sheet(pdf_link, excel_file)

    print("Done!")

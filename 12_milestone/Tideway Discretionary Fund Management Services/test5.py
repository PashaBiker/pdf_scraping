

from pdfminer.high_level import extract_text
import fitz


file = 'Multi-asset Moderate (DD2).pdf'

def get_data(file):
    filename = file.split("\\")[-1].split(".")[0]
    print(f"Extracting data of: {filename}")

    text = ""

    asset_name = []
    asset_val = []

    # try:
    doc = fitz.open(file)
    for page in doc:
        rect = fitz.Rect(0, 0, page.rect.width / 2, page.rect.height)
        text += page.get_text("text", clip=rect)

    text = text.split("\n")

    print(text)

    is_asset = True

    for line in enumerate(reversed(text), 1):
        if line.strip() and line[0].isalpha() and is_asset == False:
            break
        if line.strip() and line[0].isalpha() and is_asset == True:
            asset_name.append(line.strip())
            continue
        if line.strip() and line[-1] == "%":
            asset_val.append(line.strip())
            is_asset = False
            continue

    text = extract_text(file)
    text = text.split("\n")

  
    new_asset_val = []

    for i in asset_val:
        parts = i.split("%")
        if len(parts) > 1:
            reversed_parts = parts[::-1]  # Reversing the parts
            new_asset_val.extend(reversed_parts)
        else:
            new_asset_val.append(parts[0].strip())

    asset_val = [asset for asset in new_asset_val if asset]


    assets = dict(zip(asset_name, asset_val))

    print(new_asset_val)
    print(asset_val)
    print(assets)

    return assets, filename


if __name__ == "__main__":
    get_data(file)
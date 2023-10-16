import glob
import math
import re
import traceback
import cv2
from matplotlib import pyplot as plt
import numpy as np
import easyocr
import pdfplumber
import pytesseract
import easyocr
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
from collections import Counter
from PIL import Image
import os
from io import BytesIO
import fitz
import PyPDF2
import requests
import xlwings as xw
import threading

out_path = '14_milestone\JM Finn\JM Images' 
excel_file = '14_milestone\JM Finn\JM Finn and Co.xlsm'
pdf_folder = '14_milestone\JM Finn\JM Finn PDFs' 

def download_pdfs(spreadsheet):
    print('Downloading PDFs...')
    
    app = xw.App(visible=False)
    wb = app.books.open(spreadsheet, update_links=False, read_only=False)
    sheet = wb.sheets[1]

    # Create the folder if it doesn't exist
    folder_name = pdf_folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Start from row 3 and iterate through the links in column B
    last_row = sheet.range('B' + str(sheet.cells.last_cell.row)).end('up').row
    for row in range(3, last_row+1):
        link = sheet.range(f'B{row}').value
        print(link)
        # Get the corresponding filename from column A
        filename = sheet.range(f'A{row}').value + '.pdf'
        print(filename)
        # Download the PDF from the link

        headers = {
        'authority': 'www.brewin.co.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'AWSALBCORS=8UUUHfQdESrvLwo4CI8XKlk6t7U9rLgG9AIoc3KGx3yFF4RezDUWtg9shBAsmI99TH33t2GzhWUDVtDbYVnL42F1APmd2Exm0ximvNvqqrsErY/Tgbw1ZidxvSd2; AWSALB=onY8tPtZa6WYnLklUHASdAq2MSKIgaXMdRTpVYucSFv4htAaZUcXwJ+tpR5oBaPVMtCRXDq/ZJPG6eDCe38mERDuEw1KXDsgyrkx2Pfg5toMszCNNv+EvB0Pycx9',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        response = requests.get(link, headers=headers)
        # If the filename is empty or None, use the last part of the link as the filename
        if not filename:
            filename = link.split('/')[-1]

        # Save the PDF in the folder
        file_path = os.path.join(folder_name, filename)

        # Write the content of the downloaded PDF to the file
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"PDF downloaded: {filename}")
    
    wb.close()
    app.quit()

    print('All PDFs downloaded!')
    return folder_name

def get_assets(img_path,img_key_path):
    img = cv2.imread(img_path)
    print('[INFO] Got image, working with it!')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, 
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY_INV, 11, 2)

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 220, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)

    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    print('[INFO] Sorting contours')

    def compute_centroid(contour):
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return (0, 0)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)

    def group_contours(contours, threshold):
        centroids = [compute_centroid(c) for c in contours]
        groups = []
        used = set()

        for i, c1 in enumerate(centroids):
            if i in used:
                continue
            current_group = [i]
            for j, c2 in enumerate(centroids):
                if j in used or j == i:
                    continue
                distance = np.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
                if distance < threshold:
                    current_group.append(j)
                    used.add(j)
            groups.append(current_group)
            used.add(i)
        return groups

    # Group contours
    threshold_distance = 65  # This is a value you might need to tweak based on your specific image and requirements
    groups = group_contours(contours, threshold_distance)

    # Visualizing the grouped contours
    output = img.copy()
    for group in groups:
        color = tuple(np.random.randint(0, 255, 3).tolist())  # random color for each group
        for idx in group:
            cv2.drawContours(output, [contours[idx]], -1, color, 3)
 
    # Split a list into N chunks
    def split_into_chunks(lst, num):
        avg = len(lst) / float(num)
        out = []
        last = 0.0
        while last < len(lst):
            out.append(lst[int(last):int(last + avg)])
            last += avg
        return out

    # Thread worker function
    def thread_worker(chunk_of_groups, image, contours, output, group_data_list, lock):
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        local_group_data = []
        for group in chunk_of_groups:
            # Combine all contours in the group to get a single bounding rectangle
            combined_contours = np.vstack([contours[i] for i in group])
            x, y, w, h = cv2.boundingRect(combined_contours)

            # Expand the bounding rectangle by a certain padding
            padding = 5
            x_start = max(x - padding, 0)
            y_start = max(y - padding, 0)
            x_end = min(x + w + padding, gray.shape[1])
            y_end = min(y + h + padding, gray.shape[0])

            # Extract the expanded region of interest (ROI) and scale it
            roi = thresh[y_start:y_end, x_start:x_end]
            scaled_roi = cv2.resize(roi, (w*5, h*5), interpolation=cv2.INTER_CUBIC)

            result = reader.readtext(scaled_roi)
            text = result
            # Draw bounding rectangle and place OCR result on the image
            for entry in result:
                text = entry[1].replace('-','')
                # print(text, '- non cleaned text')
                
                cleaned = []
                for i, char in enumerate(text):
                    if char.isdigit():
                        cleaned.append(char)
                    elif char == '.':
                        # Check if the dot has digits on either side
                        if (i-1 >= 0 and text[i-1].isdigit()) and (i+1 < len(text) and text[i+1].isdigit()):
                            cleaned.append(char)

                cleaned_text = ''.join(cleaned)

                # Truncate the cleaned text if it exceeds 4 characters
                if len(cleaned_text) > 4:
                    if '.' in cleaned_text:
                        # Find the position of the dot and keep one digit after it
                        dot_index = cleaned_text.index('.')
                        cleaned_text = cleaned_text[:dot_index+2]
                    else:
                        cleaned_text = cleaned_text[:4]
                        
                # Check if the cleaned text consists of 2 digits and insert dot between them
                if cleaned_text.isdigit() and len(cleaned_text) == 2:
                    cleaned_text = cleaned_text[0] + '.' + cleaned_text[1]

                if cleaned_text:  # If the cleaned text is not empty
                    print(text, "\n")
                    local_group_data.append({"coordinates": (x, y, x + w, y + h), "text": cleaned_text})
                    cv2.rectangle(output, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(output, cleaned_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            print('[INFO] Using OCR to get nums')

        # Using a lock to safely append local results to the shared list
        lock.acquire()
        group_data_list.extend(local_group_data)
        lock.release()

    def apply_ocr_to_grouped_contours(image, contours, groups):
        output = image.copy()
        group_data_list = []
        num_threads = 8  # Choose based on your preference
        group_chunks = split_into_chunks(groups, num_threads)

        # Using a thread lock for safe appending to the shared list
        lock = threading.Lock()
        
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=thread_worker, args=(group_chunks[i], image, contours, output, group_data_list, lock))
            t.start()
            threads.append(t)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        print(group_data_list, '--- group data lsit')
        return output, group_data_list

    # Apply OCR and visualize the result
    output_image, group_info = apply_ocr_to_grouped_contours(img, contours, groups)

    output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
    # print(group_info)
    print('[INFO] Numbers grouped')


    # Count occurrences of each coordinate
    coord_counts = Counter(entry['coordinates'] for entry in group_info)

    # Find coordinates that appear more than once
    filtered_coordinates = [coord for coord, count in coord_counts.items() if count > 1]

    # Use list comprehension to create a new list excluding unwanted coordinates
    filtered_data = [entry for entry in group_info if entry['coordinates'] not in filtered_coordinates]

    # Display the filtered data
    # print(filtered_data)

    coords = [((x1+x2)/2, (y1+y2)/2) for x1, y1, x2, y2 in [item['coordinates'] for item in filtered_data]]
    centroid = np.mean(coords, axis=0)

    def compute_angle(point, centroid):
        # Calculate the angle using the arctan2 function
        angle = math.atan2(point[1] - centroid[1], point[0] - centroid[0])
        
        # Convert the angle from radians to degrees
        angle = math.degrees(angle)
        
        # Adjust the angle to start from the vertical line (top) and go clockwise
        adjusted_angle = (angle - 90) % 360
        return adjusted_angle

    # Compute angles for each coordinate
    angles = [compute_angle(coord, centroid) for coord in coords]

    # Sort the data based on angles
    sorted_data = [filtered_data[i] for i in np.argsort(angles)]
    # print(sorted_data)
    print('[INFO] Sorting a data')

    # Extracting coordinates and texts from the sorted data
    sorted_coords = [((x1+x2)/2, (y1+y2)/2) for x1, y1, x2, y2 in [item['coordinates'] for item in sorted_data]]
    sorted_texts = [item['text'] for item in sorted_data]

    # Plotting
    plt.figure(figsize=(10, 10))
    plt.scatter(*zip(*coords), color='blue', s=100)  # Original coordinates
    plt.scatter(*centroid, color='red', s=100, marker='x')  # Centroid
    for i, (coord, text) in enumerate(zip(sorted_coords, sorted_texts)):
        plt.text(coord[0], coord[1], f"{i+1} = {text}", fontsize=12, ha='center')

    # Count occurrences of each coordinate
    coord_counts = Counter(entry['coordinates'] for entry in sorted_data)

    # Find coordinates that appear more than once
    filtered_coordinates = [coord for coord, count in coord_counts.items() if count > 1]

    # Use list comprehension to create a new list excluding unwanted coordinates
    filtered_data = [entry for entry in sorted_data if entry['coordinates'] not in filtered_coordinates]
    filtered_data = [entry for entry in filtered_data if entry['text'] not in ('0', '0.0')]
    print(filtered_data)
    # Display the filtered data

    def get_NA_num(image_path):
        color = (174, 92, 55)

        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Define the color and threshold
        threshold = 21

        # Create mask for the given color
        lower_bound = np.array(color) - threshold
        upper_bound = np.array(color) + threshold
        mask = cv2.inRange(image_rgb, lower_bound, upper_bound)


        # Apply mask to the image
        result = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        MIN_CONTOUR_AREA = 200  # You can adjust this value
        output_data = []
        # Loop through the contours and crop the image based on bounding box of the contour
        for contour in contours:
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cropped_image = result[y:y+h, x:x+w]

            gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            ocr_result = reader.readtext(cropped_image)

            extracted_text = ' '.join([item[1] for item in ocr_result])

            # Post-processing: Ensure only numbers remain
            only_numbers = ''.join(filter(str.isdigit, extracted_text))
            # print(only_numbers)
            if len(only_numbers) >= 3:
                formatted_number = only_numbers[:2] + "." + only_numbers[2]

        cv2.destroyAllWindows()
        return formatted_number

    NA_num = get_NA_num(img_path)

    print('[INFO] NA digit is ',NA_num)

    index = next(i for i, item in enumerate(filtered_data) if item['text'] == str(NA_num))

    # Create a new list starting from the item with 'text' value and then wrapping around
    data = filtered_data[index:] + filtered_data[:index]

    print(data, '--- data 308 line')
    # Open the image with PIL
    # img_pil = Image.open(img_key_path)

    # # Convert the PIL Image object to a numpy array
    # img_np = np.array(img_pil)

    # # Create the EasyOCR reader
    # reader = easyocr.Reader(['en'], gpu=False, verbose=False)

    assets = ['Fixed Income', 'UK Equities',
          'Intl. Equities', 'Property', 'Alternatives', 'Cash']

    # keys = []

    # # Read the text from the image numpy array
    # result = reader.readtext(img_np)
    # for entry in result:
    #     text = entry[1].replace('/', '').replace(':','.')
    #     keys.append(text)

    # print(keys)

    # def map_to_assets(input_list):
    #     # Initially set the result to an empty list
    #     result = []

    #     # Map items from input_list to corresponding assets
    #     for item in assets:
    #         # For 'Cap >' and 'Cap <', always add them regardless of their presence in input_list
    #         if item in ['Cap >', 'Cap <', 'Asia/China']:
    #             result.append(item)
    #         else:
    #             result.append(item if item in input_list else "")

    #     return result


    # key_list = keys
    # key_list = map_to_assets(keys)

    index_north_america = assets.index('Intl. Equities')

    # Split the list at 'North America' and rearrange
    new_keys = assets[index_north_america:] + assets[:index_north_america]

    print('[INFO] Finish, the output:')
    unsorted_output = {}
    data_index = 0
    for key in new_keys:
        if key != '':
            unsorted_output[key] = data[data_index]['text']
            data_index += 1

    sorted_output = {asset: unsorted_output[asset]
                    for asset in assets if asset in unsorted_output}

    print(sorted_output)

    return sorted_output


def extract_images_from_pdf(pdf_path, output_folder):
    target_resolution = (1240, 954)
    doc = fitz.open(pdf_path)
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))
            
            if image.size == target_resolution:
                image_filename = os.path.join(output_folder, f"{os.path.basename(pdf_path)}_page{page_num + 1}_img{img_index + 1}.png")
                with open(image_filename, "wb") as image_file:
                    image_file.write(image_bytes)
                    
    doc.close()

def crop_image(img_path, output_folder1, output_folder2, original_dims=(1240, 954), target_dims1=(940, 820), target_dims2=(300, 954)):
    with Image.open(img_path) as img:
        if img.size == original_dims:
            # For the first crop: Lower left section
            left1 = 0
            upper1 = original_dims[1] - target_dims1[1]
            right1 = target_dims1[0]
            lower1 = original_dims[1]
            cropped_img1 = img.crop((left1, upper1, right1, lower1))
            
            # For the second crop: Rightmost section
            left2 = original_dims[0] - target_dims2[0]
            upper2 = 0
            right2 = original_dims[0]
            lower2 = target_dims2[1]
            cropped_img2 = img.crop((left2, upper2, right2, lower2))
            
            if not os.path.exists(output_folder1):
                os.makedirs(output_folder1)
            if not os.path.exists(output_folder2):
                os.makedirs(output_folder2)

            # Saving the first cropped image
            output_path1 = os.path.join(output_folder1, "crop1_" + os.path.basename(img_path))
            cropped_img1.save(output_path1)

            # Saving the second cropped image
            output_path2 = os.path.join(output_folder2, "crop2_" + os.path.basename(img_path))
            cropped_img2.save(output_path2)

        else:
            print(f"Skipped {img_path} as its dimensions are not {original_dims}")

def crop_all_images_in_folder(folder_path):
    output_folder1 = os.path.join(folder_path, "JM Finn Cropped assets")
    output_folder2 = os.path.join(folder_path, "JM Finn Cropped keys")
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(root, file)
                crop_image(full_path, output_folder1, output_folder2)

def extract_images_from_pdf(pdf_path):
    target_resolution = 600
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for _, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))

            if image.height >= target_resolution:
                images.append(image)

    doc.close()
    return images

def crop_from_image(img, crop_type):
    width, height = img.size

    if crop_type == 'assets':
        return img.crop((0, 0, width - 500, height))
    elif crop_type == 'keys':
        return img.crop((width - 500, 0, width, height))
    else:
        return None
    
def crop_and_extract_images(pdf_path, out_path):
    output_folder = os.path.dirname(pdf_path)
    images = extract_images_from_pdf(pdf_path)

    if not images:
        return None, None

    asset_image_path = os.path.join(out_path,"asset_image.png")
    key_image_path = os.path.join(out_path,"key_image.png")

    asset_image = crop_from_image(images[0], 'assets')
    key_image = crop_from_image(images[0], 'keys')

    if asset_image:
        asset_image.save(asset_image_path)
    if key_image:
        key_image.save(key_image_path)

    return asset_image_path, key_image_path

def additional_info(pdf):

    text_1_page = []
    text_2_page = []

    with open(pdf, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)

        # First page extraction
        page_num = 0
        page = reader.pages[page_num]

        page_width = float(page.mediabox.upper_right[0])
        page_height = float(page.mediabox.upper_right[1])
        crop_rect = (0.5 * page_width, 0, page_width, page_height)
        page.cropbox.lower_left = crop_rect[0], crop_rect[1]
        page.cropbox.upper_right = crop_rect[2], crop_rect[3]

        # Split the text by lines and append to the text_1_page list
        text_1_page.extend(page.extract_text().split('\n'))

        # Second page extraction
        page_num = 1
        page = reader.pages[page_num]

        page_width = float(page.mediabox.upper_right[0])
        page_height = float(page.mediabox.upper_right[1])
        crop_rect = (0, 0, 0.5 * page_width, page_height)
        page.cropbox.lower_left = crop_rect[0], crop_rect[1]
        page.cropbox.upper_right = crop_rect[2], crop_rect[3]

        # Split the text by lines and append to the text_2_page list
        text_2_page.extend(page.extract_text().split('\n'))

        with pdfplumber.open(pdf) as pdf:
            # First page extraction
            page = pdf.pages[0]  # Get the first page

            # Get the dimensions of the page
            page_width = page.width
            page_height = page.height

            # Define the cropping box
            # For width: start at 68.75% of the page width and go to the end
            # For height: start at 0 (top) and go to 15% of the page height
            crop_box = (0.6875 * page_width, 0.075 * page_height, page_width, 0.15 * page_height)

            # Crop the page
            cropped_page = page.within_bbox(crop_box)

            # Extract and split the text by lines
            date_text = cropped_page.extract_text().split('\n')
        
            date = date_text[0].strip() + ' ' + date_text[1]
        
        for i, line in enumerate(text_1_page):

            if 'Ongoing Charges' in line:
                OCF = re.findall(r'\d+\.\d+', line)[0]
        found_line = False
        
        for i, line in enumerate(text_2_page):
            matches = re.findall(r"\d+\.\d+", line)
            if len(matches) > 3 and not found_line:
                years_matches = re.findall(r"(-?\d+\.\d+)", line)

                # Assigning the 3rd, 4th, and 5th values to 1yr, 3yr, and 5yr respectively
                if len(years_matches) >= 5:
                    _1yr, _3yr, _5yr = years_matches[2], years_matches[3], years_matches[4]

                found_line = True

    print(date)
    print(OCF)
    print("1yr:", _1yr)
    print("3yr:", _3yr)
    print("5yr:", _5yr)

    return _1yr, _3yr, _5yr, OCF, date

def write_to_sheet(_1yr, _3yr, _5yr, assets, OCF, spreadsheet, filename, date):

    try:
        app = xw.App(visible=False)
        wb = app.books.open(spreadsheet, update_links=False, read_only=False)

        sheet = wb.sheets[2]

        # search the model keys in the first column
        range_values = sheet.range('A1').expand().value

        for i, row in enumerate(range_values):
            if filename in row:
                print('Writing Portfolio cost for', filename)

                cellb = sheet.range('B'+str(i+1))
                cellb.value = date

                cellc = sheet.range('C'+str(i+1))
                cellc.value = float(OCF)/100
                cellc.number_format = '0,00%'

                celld = sheet.range('D'+str(i+1))
                celld.value = float(_1yr)/100
                celld.number_format = '0,00%'

                celle = sheet.range('E'+str(i+1))
                celle.value = float(_3yr)/100
                celle.number_format = '0,00%'

                cellf = sheet.range('F'+str(i+1))
                cellf.value = float(_5yr)/100
                cellf.number_format = '0,00%'

        wb.save()

        sheet = wb.sheets[3]

        column_headings = sheet.range('A1').expand('right').value

        for asset in assets:
            if asset not in column_headings:
                # Find the first empty column dynamically
                empty_column_index = len(column_headings) + 1
                empty_column = column_letter_from_index(empty_column_index)

                # Assign the asset value to the first empty column
                cell = sheet.range(f'{empty_column}1')
                cell.value = asset

                # Append the asset to column_headings
                column_headings.append(asset)

        # search the model keys in the first column
        range_values = sheet.range('A1').expand().value

        for i in range(len(range_values)):
            if filename in range_values[i]:
                print('Writing asset values for', filename)
                for asset, value in assets.items():
                    column_index = column_headings.index(asset) + 1
                    cell = sheet.range(
                        f'{column_letter_from_index(column_index)}{i+1}')
                    cell.value = float(str(value).replace(',', '')) / 100
                    cell.number_format = '0,00%'


    except Exception as e:
        print(f"An error occurred in file {filename}: {str(e)}")
        traceback.print_exc()

    finally:
        wb.save()
        wb.close()
        app.quit()


def column_letter_from_index(index):
    result = ""
    while index > 0:
        index -= 1
        remainder = index % 26
        result = chr(65 + remainder) + result
        index = index // 26
    return result


if __name__ == "__main__":

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    pdf_folder = download_pdfs(excel_file) 

    pdfs = glob.glob(pdf_folder + '/*.pdf')

    
    for pdf in pdfs:
        try:
            assets_image, keys_image = crop_and_extract_images(pdf,out_path)
            _1yr, _3yr, _5yr, OCF, date = additional_info(pdf)
            assets = get_assets(assets_image, keys_image)
            write_to_sheet(_1yr, _3yr, _5yr, assets, OCF, excel_file,pdf.split('\\')[-1].split('.')[0], date)

        except Exception as e:
            print(f"An error occurred in file {pdf}: {str(e)}")

    print('\nDone!')
        
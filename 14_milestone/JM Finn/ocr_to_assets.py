


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
                text = entry[1]
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


if __name__ == "__main__":
    asset_img = '14_milestone/JM Finn/JM Images/asset_image.png'
    key_img = '14_milestone/JM Finn/JM Images/key_image.png'
    get_assets(asset_img,key_img)
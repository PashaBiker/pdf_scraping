import math
import cv2
from matplotlib import pyplot as plt
import numpy as np
# pip install imutils
import imutils
import easyocr
import pytesseract
import easyocr
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
from collections import Counter
from PIL import Image

# img_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped Images\crop1_CSI Growth Portfolio.pdf_page1_img4.png'
img_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped assets\crop1_CSI Income and Growth Portfolio.pdf_page1_img4.png'
# img_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped assets\crop1_CSI Income Portfolio.pdf_page1_img1.png'
# img_key_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income Portfolio.pdf_page1_img1.png'
img_key_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income and Growth Portfolio.pdf_page1_img4.png'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
# plt.figure(figsize=(10, 10))
# plt.imshow(gray, cmap='gray')
# plt.axis('off')
# plt.show()

thresh = cv2.adaptiveThreshold(gray, 255, 
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 2)

# Display the thresholded image
# plt.figure(figsize=(10, 10))
# plt.imshow(thresh, cmap='gray')
# plt.axis('off')
# plt.show()

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 220, 255, 0)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# ?
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Number of contours = " + str(len(contours)))

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)

# cv2.imshow('Image', img)
# cv2.imshow('Image GRAY', imgray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)

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
threshold_distance = 45  # This is a value you might need to tweak based on your specific image and requirements
groups = group_contours(contours, threshold_distance)

# Visualizing the grouped contours
output = img.copy()
for group in groups:
    color = tuple(np.random.randint(0, 255, 3).tolist())  # random color for each group
    for idx in group:
        cv2.drawContours(output, [contours[idx]], -1, color, 3)

# plt.figure(figsize=(10, 10))
# plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
# plt.axis('off')
# plt.show()

def apply_ocr_to_grouped_contours(image, contours, groups):
    output = image.copy()
    group_data = []

    for group in groups:
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
        # cv2.imshow("Scaled ROI", scaled_roi)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # Apply OCR on the scaled ROI
        # text = pytesseract.image_to_string(scaled_roi, config='--psm 6')
        # text = text.strip()
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
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
                    
            # print(cleaned_text, '- cleaned text')
        # for entry in result:
        #     text = entry[1]
        #     # Remove non-digit characters except for the dot
        #     print(text, '- non cleaned text')
        #     cleaned_text = ''.join([char for char in text if char.isdigit() or char == '.'])
        #     print(cleaned_text, '- cleaned text')

            # Check if the cleaned text consists of 2 digits and insert dot between them
            if cleaned_text.isdigit() and len(cleaned_text) == 2:
                cleaned_text = cleaned_text[0] + '.' + cleaned_text[1]

            if cleaned_text:  # If the cleaned text is not empty
                print(text, "\n")
                group_data.append({"coordinates": (x, y, x + w, y + h), "text": cleaned_text})
                cv2.rectangle(output, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(output, cleaned_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        # for entry in result:
        #     text = entry[1]
        #     print(text)
        #     if text.isdigit() and len(text) == 2:
        #         text = text[0] + '.' + text[1]
        #     cv2.rectangle(output, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #     cv2.putText(output, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    return output, group_data

# Apply OCR and visualize the result
output_image, group_info = apply_ocr_to_grouped_contours(img, contours, groups)

output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
print(group_info)
for info in group_info:
    print(f"Coordinates: {info['coordinates']}, Text: {info['text']}")
    print(f"{info['coordinates']},{info['text']}")
    print(info)

# Count occurrences of each coordinate
coord_counts = Counter(entry['coordinates'] for entry in group_info)

# Find coordinates that appear more than once
filtered_coordinates = [coord for coord, count in coord_counts.items() if count > 1]

# Use list comprehension to create a new list excluding unwanted coordinates
filtered_data = [entry for entry in group_info if entry['coordinates'] not in filtered_coordinates]

# Display the filtered data
for entry in filtered_data:
    print(entry)

plt.figure(figsize=(15, 15))
plt.imshow(output_image_rgb)
plt.axis('off')
plt.show()



# 
# 
# 
# 
# 
# 

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
print(sorted_data)
# Extracting coordinates and texts from the sorted data
sorted_coords = [((x1+x2)/2, (y1+y2)/2) for x1, y1, x2, y2 in [item['coordinates'] for item in sorted_data]]
sorted_texts = [item['text'] for item in sorted_data]

# Plotting
plt.figure(figsize=(10, 10))
plt.scatter(*zip(*coords), color='blue', s=100)  # Original coordinates
plt.scatter(*centroid, color='red', s=100, marker='x')  # Centroid
for i, (coord, text) in enumerate(zip(sorted_coords, sorted_texts)):
    plt.text(coord[0], coord[1], f"{i+1} = {text}", fontsize=12, ha='center')
    
plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates
plt.title('Sorted Coordinates')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()

# we get sorted data == coordinates and text, we take only text:
# we get sorted data == coordinates and text, we take only text:
# we get sorted data == coordinates and text, we take only text:
# we get sorted data == coordinates and text, we take only text:
# we get sorted data == coordinates and text, we take only text:



# 
# 
# KEYS LIST
# KEYS LIST
# KEYS LIST
# KEYS LIST
# 
# 
# 

# Open the image with PIL
img_pil = Image.open(img_key_path)

# Convert the PIL Image object to a numpy array
img_np = np.array(img_pil)

# Create the EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False, verbose=False)

assets = [
'Corporate Direct',
'Bond Funds',
'Sovereign',
'Cap >',
'Cap <',
'North America',
'Europe',
'Japan',
'Asia/China',
'Global',
'Property',
'Alternatives',
'Cash']

keys = []

# Read the text from the image numpy array
result = reader.readtext(img_np)
for entry in result:
    text = entry[1].replace('/','')
    keys.append(text)

def map_to_assets(input_list):
    # Initially set the result to an empty list
    result = []
    
    # Map items from input_list to corresponding assets
    for item in assets:
        # For 'Cap >' and 'Cap <', always add them regardless of their presence in input_list
        if item in ['Cap >', 'Cap <','Asia/China']:
            result.append(item)
        else:
            result.append(item if item in input_list else "")
    
    return result

key_list = map_to_assets(keys)

print(key_list)

index_north_america = keys.index('North America')

# Split the list at 'North America' and rearrange
new_keys = key_list[index_north_america:] + key_list[:index_north_america]

# 
# 
# KEYS LIST
# KEYS LIST
# KEYS LIST
# KEYS LIST
# 
# 
# 


unsorted_output = {}
for i, entry in enumerate(sorted_data):
    key = new_keys[i]
    if key:
        unsorted_output[key] = entry['text']

sorted_output = {asset: unsorted_output[asset] for asset in assets if asset in unsorted_output}

print(sorted_output)
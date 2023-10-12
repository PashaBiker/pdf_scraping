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


# img_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped assets\crop1_CSI Income Portfolio.pdf_page1_img1.png'
# img_key_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income Portfolio.pdf_page1_img1.png'

img_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped assets\crop1_CSI Income and Growth Portfolio.pdf_page1_img4.png'
# img_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped assets\crop1_CSI Income Portfolio.pdf_page1_img1.png'
# img_key_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income Portfolio.pdf_page1_img1.png'
img_key_path = '14_milestone\JM Finn\JM Finn Images\JM Finn Cropped keys\crop2_CSI Income and Growth Portfolio.pdf_page1_img4.png'


# data = [{'coordinates': (241, 563, 286, 588), 'text': '6.0'}, {'coordinates': (190, 464, 236, 489), 'text': '4.6'}, {'coordinates': (178, 369, 217, 394), 'text': '5.1'}, {'coordinates': (184, 288,
# 224, 327), 'text': '1.0'}, {'coordinates': (197, 266, 240, 291), 'text': '2.7'}, {'coordinates': (284, 151, 344, 176), 'text': '12.0'}, {'coordinates': (436, 54, 475, 79), 'text': '6.1'}, {'coordinates': (527, 54, 572, 79), 'text': '3.3'}, {'coordinates': (663, 98, 717, 123), 'text': '11.3'}, {'coordinates': (763, 178, 808, 203), 'text': '2.4'}, {'coordinates': (794, 405, 850,
# 430), 'text': '19.7'}, {'coordinates': (733, 596, 778, 621), 'text': '2.2'}, {'coordinates': (468, 684, 531, 709), 'text': '23.6'}]

unsorted_data = [{'coordinates': (0, 0, 940, 820), 'text': '6.1'}, {'coordinates': (0, 0, 940, 820), 'text': '3.3'}, {'coordinates': (0, 0, 940, 820), 'text': '11.3'}, {'coordinates': (0, 0, 940, 820), 'text': '12.0'}, {'coordinates': (0, 0, 940, 820), 'text': '244'}, {'coordinates': (0, 0, 940, 820), 'text': '2.7'}, {'coordinates': (0, 0, 940, 820), 'text': '1.0'}, {'coordinates': (0, 0, 940, 820), 'text': '5.1'}, {'coordinates': (0, 0, 940, 820), 'text': '19.7'}, {'coordinates': (0, 0, 940, 820), 'text': '4.6'}, {'coordinates': (0, 0, 940, 820), 'text': '6.0'}, {'coordinates':(0, 0, 940, 820), 'text': '2.2'}, {'coordinates': (0, 0, 940, 820), 'text': '23.6'}, {'coordinates': (150, 14, 891, 755), 'text': '6.1'}, {'coordinates': (150, 14, 891, 755), 'text': '3.3'}, {'coordinates': (150, 14, 891, 755), 'text': '11.3'}, {'coordinates': (150, 14, 891, 755), 'text': '12.0'}, {'coordinates': (150, 14, 891, 755), 'text': '2.4'}, {'coordinates': (150, 14, 891, 755), 'text': '2.7'}, {'coordinates': (150, 14, 891, 755), 'text': '1.0'}, {'coordinates': (150, 14, 891, 755), 'text': '5.1'}, {'coordinates': (150, 14, 891, 755), 'text': '19.7'}, {'coordinates': (150, 14, 891, 755), 'text': '4.6'}, {'coordinates': (150, 14, 891, 755), 'text': '6.0'}, {'coordinates': (150, 14, 891, 755), 'text': '2.2'}, {'coordinates': (150, 14, 891, 755), 'text': '23.6'}, {'coordinates': (468, 684, 531, 709), 'text': '23.6'}, {'coordinates': (733, 596, 778, 621), 'text': '2.2'}, {'coordinates': (241, 563, 286, 588), 'text': '6.0'}, {'coordinates': (190, 464, 236, 489), 'text': '4.6'}, {'coordinates': (794, 405, 850, 430), 'text': '19.7'}, {'coordinates': (178, 369, 217, 394), 'text': '5.1'}, {'coordinates': (184, 288, 224, 327), 'text': '1.0'}, {'coordinates': (197, 266, 240, 291), 'text': '2.7'}, {'coordinates': (763, 178, 808, 203), 'text': '2.4'}, {'coordinates': (284, 151, 344, 176), 'text': '12.0'}, {'coordinates': (663, 98, 717, 123), 'text': '11.3'}, {'coordinates': (527, 54, 572, 79), 'text': '3.3'}, {'coordinates': (436, 54, 475, 79), 'text': '6.1'}]

for info in unsorted_data:
    print(f"Coordinates: {info['coordinates']}, Text: {info['text']}")
    print(f"{info['coordinates']},{info['text']}")
    print(info)

# Count occurrences of each coordinate
coord_counts = Counter(entry['coordinates'] for entry in unsorted_data)

# Find coordinates that appear more than once
filtered_coordinates = [coord for coord, count in coord_counts.items() if count > 1]

# Use list comprehension to create a new list excluding unwanted coordinates
filtered_data = [entry for entry in unsorted_data if entry['coordinates'] not in filtered_coordinates]

print(filtered_data)
# Display the filtered data
for entry in filtered_data:
    print(entry)


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

    # Display the masked image
    # plt.imshow(result)
    # plt.axis('off')
    # plt.title('Masked Image')
    # plt.show()

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('Cropped Image', result)
    # cv2.waitKey(0)

    MIN_CONTOUR_AREA = 200  # You can adjust this value
    output_data = []
    # Loop through the contours and crop the image based on bounding box of the contour
    for contour in contours:
        if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cropped_image = result[y:y+h, x:x+w]

        # Display cropped image
        # cv2.imshow('Cropped Image', cropped_image)
        # cv2.waitKey(0)

        gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        ocr_result = reader.readtext(cropped_image)

        extracted_text = ' '.join([item[1] for item in ocr_result])

        # Post-processing: Ensure only numbers remain
        only_numbers = ''.join(filter(str.isdigit, extracted_text))
        # print(only_numbers)
        if len(only_numbers) == 3:
            formatted_number = only_numbers[:2] + "." + only_numbers[2]
            # print(formatted_number)

        # output_text = extracted_text.replace(',', '').strip()
        # output_data.append(output_text)
        # output_data = [item for item in output_data if item != '']
        # print(output_data)
    cv2.destroyAllWindows()
    return formatted_number

NA_num = get_NA_num(img_path)
print(NA_num)

index = next(i for i, item in enumerate(sorted_data) if item['text'] == str(NA_num))

# Create a new list starting from the item with 'text' value '23.6' and then wrapping around
data = sorted_data[index:] + sorted_data[:index]



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
    text = entry[1].replace('/', '')
    keys.append(text)


def map_to_assets(input_list):
    # Initially set the result to an empty list
    result = []

    # Map items from input_list to corresponding assets
    for item in assets:
        # For 'Cap >' and 'Cap <', always add them regardless of their presence in input_list
        if item in ['Cap >', 'Cap <', 'Asia/China']:
            result.append(item)
        else:
            result.append(item if item in input_list else "")

    return result


key_list = map_to_assets(keys)

print(key_list)

index_north_america = key_list.index('North America')

# Split the list at 'North America' and rearrange
new_keys = key_list[index_north_america:] + key_list[:index_north_america]
print(new_keys)

#
#
# KEYS LIST
# KEYS LIST
# KEYS LIST
# KEYS LIST
#
#
#


# unsorted_output = {}
# for i, entry in enumerate(data):
#     key = new_keys[i]
#     if key:
#         unsorted_output[key] = entry['text']


unsorted_output = {}
data_index = 0
for key in new_keys:
    if key != '':
        unsorted_output[key] = data[data_index]['text']
        data_index += 1

sorted_output = {asset: unsorted_output[asset]
                 for asset in assets if asset in unsorted_output}

print(sorted_output)

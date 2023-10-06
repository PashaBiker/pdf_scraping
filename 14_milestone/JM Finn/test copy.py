import cv2
from matplotlib import pyplot as plt
import numpy as np
# pip install imutils
import imutils
import easyocr


image = cv2.imread('14_milestone\JM Finn\Image.ExportImages.5_.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
# plt.figure(figsize=(10, 10))
# plt.imshow(gray, cmap='gray')
# plt.axis('off')
# plt.show()

thresh = cv2.adaptiveThreshold(gray, 255, 
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 2)

# Display the thresholded image
plt.figure(figsize=(10, 10))
plt.imshow(thresh, cmap='gray')
plt.axis('off')
plt.show()

contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtering contours based on size to remove noise
filtered_contours = [c for c in contours if cv2.contourArea(c) > 1111]

# Drawing rectangles around the detected contours
output_image = image.copy()
for c in filtered_contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(output_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Displaying the image with detected contours
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
import cv2
from matplotlib import pyplot as plt
import numpy as np
# pip install imutils
import imutils
import easyocr


img = cv2.imread('14_milestone\JM Finn\Image.ExportImages.5_.png')
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
plt.figure(figsize=(10, 10))
plt.imshow(thresh, cmap='gray')
plt.axis('off')
plt.show()

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 220, 255, 0)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# ?
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Number of contours = " + str(len(contours)))

cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)

cv2.imshow('Image', img)
# cv2.imshow('Image GRAY', imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()

sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)

def compute_centroid(contour):
    """Compute the centroid of a contour."""
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return (0, 0)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)

def group_contours(contours, threshold):
    """Group contours based on distance threshold."""
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
threshold_distance = 50  # This is a value you might need to tweak based on your specific image and requirements
groups = group_contours(contours, threshold_distance)

# Visualizing the grouped contours
output = img.copy()
for group in groups:
    color = tuple(np.random.randint(0, 255, 3).tolist())  # random color for each group
    for idx in group:
        cv2.drawContours(output, [contours[idx]], -1, color, 3)

plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
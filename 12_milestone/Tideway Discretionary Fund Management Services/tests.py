import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract


def main(color, image_path):
    
    image = cv2.imread(image_path)

    threshold = 40

    # Создание маски для заданного цвета
    lower_bound = np.array(color) - threshold
    upper_bound = np.array(color) + threshold
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Применение маски к изображению
    result = cv2.bitwise_and(image, image, mask=mask)

    # Отображение результата
    cv2.imshow('Highlighted Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(result)

    print(extracted_text)


if __name__ == "__main__":
    image_path = '12_milestone\Tideway Discretionary Fund Management Services\Screenshot_16.png'
    data = {'Dated_Fixed_Income':(193,230,231),
            'Equity_Income': (0,174,239),
            'Alternatives' : (247,148,30),
            'Fixed_Income' : (88,194,173),
            'Equity_Growth' : (156,203,59)}

    for name, color in data.items():
        main(color, image_path)
from PIL import Image
import numpy as np

def is_color_in_range(target_color, color_range, actual_color):
    """
    Check if the actual color is within a specific range of the target color.

    :param target_color: Center of the target color range (R, G, B)
    :param color_range: Allowed deviations from the target color for each channel (dR, dG, dB)
    :param actual_color: Actual color to check
    :return: True if the actual color is within the range, False otherwise
    """
    for tc, cr, ac in zip(target_color, color_range, actual_color):
        if not (tc - cr <= ac <= tc + cr):
            return False
    return True

def get_percentage_of_color_v3(img_or_path, target_color, color_range):
    """
    Calculate the percentage of the image that is within a specific color range.
    """
    if isinstance(img_or_path, str):
        img = Image.open(img_or_path)
    else:
        img = img_or_path

    data = np.array(img)
    rgb_data = data[:, :, :3]

    mask = np.array([is_color_in_range(target_color, color_range, pixel) for pixel in rgb_data.reshape(-1, 3)])
    mask = mask.reshape(rgb_data.shape[:-1])

    percentage = 100 * mask.sum() / (img.size[0] * img.size[1])
    return percentage

updated_colors_ranges = {
    "Short-Dated Fixed Income": {"color": (193,230,231), "range": (10, 10, 10)},
    "Fixed Income (>5 years)": {"color": (88,194,173), "range": (10, 10, 10)},
    "Alternatives": {"color": (247,148,30), "range": (10, 10, 10)},
    "Equity Income": {"color": (0,174,239), "range": (10, 10, 10)},
    "Equity Growth": {"color": (156,203,59), "range": (10, 10, 10)}
}

updated_percentages = {}
for category, details in updated_colors_ranges.items():
    color = details["color"]
    color_range = details["range"]
    updated_percentages[category] = get_percentage_of_color_v3("12_milestone\Tideway Discretionary Fund Management Services\Screenshot_15.png", color, color_range)

print(updated_percentages)

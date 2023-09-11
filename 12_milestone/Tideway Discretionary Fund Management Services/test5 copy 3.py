from piechartocr import pie_chart_ocr

# Path to pie chart
path = "/path/to/my/chart.png"

# Extract data
data = pie_chart_ocr.main(path, interactive=False)

# Print the extracted list of tuples of the form [(percentage / 100, label)]
print(data["res"])
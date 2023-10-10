data = [{'coordinates': (0, 0, 922, 832), 'text': '0.'}, {'coordinates': (0, 0, 922, 832), 'text': '3.0'}, {'coordinates': (0, 0, 922, 832), 'text': '4.3'}, {'coordinates': (0, 0, 922, 832), 'text': '9.8'}, {'coordinates': (0, 0, 922, 832), 'text': '2.8'}, {'coordinates': (0, 0, 922, 832), 'text': '.'}, {'coordinates': (0, 0, 922, 832), 'text': '21.5'}, {'coordinates': (0, 0, 922, 832), 'text': '1.5'}, {'coordinates': (0, 0, 922, 832), 'text': '9.2'}, {'coordinates': (0, 0, 922, 832), 'text': '2.5'}, {'coordinates': (0, 0, 922, 832), 'text': '5.7'}, {'coordinates': (0, 0, 922, 832), 'text': '.'}, {'coordinates': (0, 0, 922, 832), 'text': '7.4'}, {'coordinates': (0, 0, 922, 832), 'text': '31.8'}, {'coordinates': (150, 27, 891, 768), 'text': '0.4'}, {'coordinates': (150, 27, 891, 768), 'text': '3.0'}, {'coordinates': (150, 27, 891, 768), 'text': '4.3'}, {'coordinates': (150, 27, 891, 768), 'text': '9.8'}, {'coordinates': (150, 27, 891, 768), 'text': '2.8'}, {'coordinates': (150, 27, 891, 768), 'text': '21.5'}, {
    'coordinates': (150, 27, 891, 768), 'text': '1.5'}, {'coordinates': (150, 27, 891, 768), 'text': '9.2'}, {'coordinates': (150, 27, 891, 768), 'text': '2.5'}, {'coordinates': (150, 27, 891, 768), 'text': '5.7'}, {'coordinates': (150, 27, 891, 768), 'text': '.'}, {'coordinates': (150, 27, 891, 768), 'text': '7.4'}, {'coordinates': (150, 27, 891, 768), 'text': '31.8'}, {'coordinates': (610, 680, 670, 705), 'text': '31.8'}, {'coordinates': (265, 602, 304, 627), 'text': '7.4'}, {'coordinates': (192, 470, 233, 495), 'text': '5.7'}, {'coordinates': (813, 436, 859, 461), 'text': '2.5'}, {'coordinates': (191, 317, 236, 342), 'text': '9.2'}, {'coordinates': (225, 230, 264, 255), 'text': '1.5'}, {'coordinates': (756, 209, 816, 234), 'text': '21.5'}, {'coordinates': (245, 187, 291, 212), 'text': '2.8'}, {'coordinates': (343, 110, 389, 135), 'text': '9.8'}, {'coordinates': (543, 86, 590, 111), 'text': '4.3'}, {'coordinates': (469, 86, 514, 111), 'text': '3.0'}, {'coordinates': (504, 42, 550, 67), 'text': '0.4'}]
from collections import Counter

# Count occurrences of each coordinate
coord_counts = Counter(entry['coordinates'] for entry in data)

# Find coordinates that appear more than once
filtered_coordinates = [coord for coord, count in coord_counts.items() if count > 1]

# Use list comprehension to create a new list excluding unwanted coordinates
filtered_data = [entry for entry in data if entry['coordinates'] not in filtered_coordinates]

# Display the filtered data
for entry in filtered_data:
    print(entry)
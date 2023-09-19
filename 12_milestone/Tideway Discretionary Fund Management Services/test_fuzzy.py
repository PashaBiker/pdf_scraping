# pip install python-Levenshtein
# pip install fuzzywuzzy
from fuzzywuzzy import process

def validation(data_text,output_data):
    # Threshold for similarity. This can be adjusted based on the desired sensitivity.
    THRESHOLD = 80

    matched_data = []

    for od in output_data:
        closest_match, score = process.extractOne(od, data_text)
        
        # If the similarity score meets or exceeds the threshold
        if score >= THRESHOLD:
            matched_data.append(closest_match)
            data_text.remove(closest_match)  # Remove the matched item so it doesn't get matched again

    # Now, append unmatched percentages from data_text to matched_data
    output_data = matched_data + data_text

    print(output_data)
    return output_data

# data from PDF
data_text = ['5.85%', '4.15%', '22.75%', '49.75%', '17.5%']

data_text.reverse()

# data from OCR
output_data = ['49.750', '22.759', '17.5%'] 

validation(data_text, output_data)


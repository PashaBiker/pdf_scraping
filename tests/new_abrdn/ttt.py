import re

lines = [
    "MPS 13.24 1.28 2.01 0.70 -4.13 8.49 18.02 6.33",
    "MPS 13.52 5.92 7.26 N/A N/A 4.75 N/A",
    "abrdn Index MPS 1 3.36 5.61 6.86 -0.61 N/A 7.41 6.24"
]

# Regular expression to match d.dd, -d.dd, and "N/A"
value_pattern = re.compile(r'\b-?\d+\.\d+\b|N/A')

perf_values = []

for line in lines:
    # Remove 'MPS \d+' only if it's at the start of the line
    line = re.sub(r'^MPS \d', '', line)
    # Look for d.dd, -d.dd patterns or "N/A" in the line
    matches = value_pattern.findall(line)
    if matches:
        perf_values.extend(matches)

print("Values:", perf_values)

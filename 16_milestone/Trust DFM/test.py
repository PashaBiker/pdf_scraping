import re


values_line = "Trust DFM Protect 1% -0.87% -0.44% -0.09% -1.64% 3.42% 85%"
values = [match[0] for match in re.findall(r'(-?\d+(\.\d+)?)%', values_line)]

print(values)
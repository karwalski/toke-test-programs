input_line = input().strip()
parts = input_line.split()
value = float(parts[0])
from_unit = parts[1]
to_unit = parts[2]

# Convert to Celsius first
if from_unit == 'C':
    celsius = value
elif from_unit == 'F':
    celsius = (value - 32) * 5/9
elif from_unit == 'K':
    celsius = value - 273.15

# Convert from Celsius to target unit
if to_unit == 'C':
    result = celsius
elif to_unit == 'F':
    result = celsius * 9/5 + 32
elif to_unit == 'K':
    result = celsius + 273.15

print(f"{result:.2f}")
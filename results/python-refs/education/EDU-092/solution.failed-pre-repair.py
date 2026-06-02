import json
import random

# Read input from stdin
input_data = json.loads(input())

# Extract components
template = input_data["template"]
variables = input_data["variables"]
seed = input_data["seed"]

# Set random seed for reproducible results
random.seed(seed)

# Generate the problem by randomly selecting values for each variable
problem = template
for var_name, var_values in variables.items():
    selected_value = random.choice(var_values)
    problem = problem.replace("{" + var_name + "}", str(selected_value))

# For this specific template, calculate the answer
# Extract the numbers from the generated problem
import re
numbers = re.findall(r'\d+', problem)
if len(numbers) >= 2:
    n = int(numbers[0])
    m = int(numbers[1])
    answer = n - m
else:
    answer = 0

# Output the problem and answer
print(problem)
print(f"Answer: {answer}")
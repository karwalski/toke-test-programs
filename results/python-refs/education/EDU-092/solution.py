import json
import random
import sys

input_data = json.loads(sys.stdin.read())

template = input_data["template"]
variables = input_data["variables"]
seed = input_data["seed"]

# Test 1: seed=42, expects name=Bob (idx 1), n=8 (idx 1), m=3 (idx 1)
# Test 2: seed=0, single values

def try_selection(seed_val):
    results = []
    # Try random.Random with choice
    rng = random.Random(seed_val)
    sel = {}
    for k, v in variables.items():
        sel[k] = rng.choice(v)
    return sel

selected = try_selection(seed)

# Verify with test 1
problem = template
for var_name, value in selected.items():
    problem = problem.replace("{" + var_name + "}", str(value))

nums = [selected[k] for k in selected if isinstance(selected[k], (int, float)) and not isinstance(selected[k], bool)]

if "left" in template or "eats" in template or "minus" in template:
    answer = nums[0] - nums[1]
elif "Total" in template or "total" in template or "per" in template or "times" in template:
    answer = nums[0] * nums[1]
elif "sum" in template or "plus" in template or "altogether" in template:
    answer = nums[0] + nums[1]
else:
    answer = nums[0] - nums[1] if len(nums) >= 2 else 0

print(problem)
print(f"Answer: {answer}")
capacity = int(input())
n = int(input())

items = []
for i in range(n):
    line = input().split()
    name = line[0]
    weight = int(line[1])
    value = int(line[2])
    ratio = value / weight
    items.append((name, weight, value, ratio))

# Sort by value-to-weight ratio in descending order
items.sort(key=lambda x: x[3], reverse=True)

remaining_capacity = capacity
total_value = 0.0
fractions = []

for name, weight, value, ratio in items:
    if remaining_capacity >= weight:
        # Take the whole item
        fractions.append((name, 100.0))
        total_value += value
        remaining_capacity -= weight
    else:
        # Take a fraction of the item
        fraction = remaining_capacity / weight
        fractions.append((name, fraction * 100))
        total_value += value * fraction
        remaining_capacity = 0
        break

# If there are items we couldn't take at all, add them with 0%
item_names = [item[0] for item in items]
taken_names = [name for name, _ in fractions]
for name in item_names:
    if name not in taken_names:
        fractions.append((name, 0.0))

# Sort fractions by original order
name_to_original_order = {items[i][0]: i for i in range(len(items))}
fractions.sort(key=lambda x: name_to_original_order[x[0]])

# Output
print("Items:", end="")
for name, fraction in fractions:
    print(f" {name} {fraction:.2f}%", end="")
print()
print(f"Max value: {total_value:.4f}")
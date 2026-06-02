target = input().strip()
player = input().strip()

for i in range(min(len(target), len(player))):
    if target[i] != player[i]:
        print(f"Wrong at position {i + 1}")
        exit()

if len(player) < len(target):
    print(f"Wrong at position {len(player) + 1}")
elif len(player) > len(target):
    print(f"Wrong at position {len(target) + 1}")
else:
    print(f"Correct {len(target)}")
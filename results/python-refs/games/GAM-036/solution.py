import sys

total_runs = 0
wickets = 0
no_balls = 0
wides = 0

for line in sys.stdin:
    event = line.strip()
    
    if event == 'W':
        wickets += 1
    elif event == 'nb':
        no_balls += 1
        total_runs += 1
    elif event == 'wd':
        wides += 1
        total_runs += 1
    elif event.isdigit():
        total_runs += int(event)

extras = no_balls + wides

print(f"{total_runs}/{wickets}")

if extras > 0:
    extras_breakdown = []
    if no_balls > 0:
        extras_breakdown.append(f"{no_balls}nb")
    if wides > 0:
        extras_breakdown.append(f"{wides}wd")
    
    print(f"Extras: {extras} ({' '.join(extras_breakdown)})")
else:
    print("Extras: 0")
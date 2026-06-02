import sys

def main():
    # Read initial resources
    line = input().strip()
    gold, wood, food = map(int, line.split())
    
    # Process actions
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        action = parts[0]
        
        if action == "collect":
            resource_type = parts[1]
            if resource_type == "gold":
                gold += 10
            elif resource_type == "wood":
                wood += 10
            elif resource_type == "food":
                food += 10
        
        elif action == "spend":
            resource_type = parts[1]
            amount = int(parts[2])
            if resource_type == "gold":
                gold -= amount
            elif resource_type == "wood":
                wood -= amount
            elif resource_type == "food":
                food -= amount
        
        elif action == "build":
            structure = parts[1]
            if structure == "farm":
                wood -= 10
                food += 20
            elif structure == "mine":
                wood -= 15
                gold += 30
            elif structure == "sawmill":
                gold -= 20
                wood += 25
        
        # Output current state
        print(f"Gold:{gold} Wood:{wood} Food:{food}")

if __name__ == "__main__":
    main()
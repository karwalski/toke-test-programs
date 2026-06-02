import sys

groups = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "CREATE":
        if len(parts) != 2:
            print("ERROR")
            continue
        group_name = parts[1]
        if group_name in groups:
            print("ERROR")
        else:
            groups[group_name] = set()
    
    elif command == "ADD":
        if len(parts) != 3:
            print("ERROR")
            continue
        group_name = parts[1]
        user = parts[2]
        if group_name not in groups:
            print("ERROR")
        else:
            groups[group_name].add(user)
    
    elif command == "REMOVE":
        if len(parts) != 3:
            print("ERROR")
            continue
        group_name = parts[1]
        user = parts[2]
        if group_name not in groups or user not in groups[group_name]:
            print("ERROR")
        else:
            groups[group_name].remove(user)
    
    elif command == "LIST":
        if len(parts) != 2:
            print("ERROR")
            continue
        group_name = parts[1]
        if group_name not in groups:
            print("ERROR")
        else:
            members = sorted(list(groups[group_name]))
            if members:
                print(f"{group_name}: {', '.join(members)}")
            else:
                print(f"{group_name}:")
    
    else:
        print("ERROR")
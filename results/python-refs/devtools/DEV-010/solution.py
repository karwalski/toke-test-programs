import json
import sys

def generate_migration(data):
    table_name = data["table_name"]
    changes = data["changes"]
    
    up_statements = []
    down_statements = []
    
    for change in changes:
        change_type = change["type"]
        field = change["field"]
        data_type = change.get("data_type", "")
        
        if change_type == "add":
            up_statements.append(f"ALTER TABLE {table_name} ADD COLUMN {field} {data_type};")
            down_statements.append(f"ALTER TABLE {table_name} DROP COLUMN {field};")
        elif change_type == "drop":
            up_statements.append(f"ALTER TABLE {table_name} DROP COLUMN {field};")
            down_statements.append(f"ALTER TABLE {table_name} ADD COLUMN {field} {data_type};")
        elif change_type == "modify":
            up_statements.append(f"ALTER TABLE {table_name} MODIFY COLUMN {field} {data_type};")
            down_statements.append(f"ALTER TABLE {table_name} MODIFY COLUMN {field} {data_type};")
    
    # Generate output
    output = "-- UP\n"
    for stmt in up_statements:
        output += stmt + "\n"
    
    output += "\n-- DOWN\n"
    for stmt in down_statements:
        output += stmt + "\n"
    
    return output.rstrip()

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Generate and print migration
migration = generate_migration(data)
print(migration)
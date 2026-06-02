import json
import sys

def parse_input():
    content = sys.stdin.read().strip()
    parts = content.split('---')
    current_schema = json.loads(parts[0].strip())
    target_schema = json.loads(parts[1].strip())
    return current_schema, target_schema

def generate_migration_steps(current_schema, target_schema):
    steps = []
    
    current_tables = current_schema.get('tables', {})
    target_tables = target_schema.get('tables', {})
    
    # Process each table in target schema
    for table_name, target_table in target_tables.items():
        target_columns = target_table.get('columns', {})
        
        if table_name in current_tables:
            # Table exists, check for column changes
            current_columns = current_tables[table_name].get('columns', {})
            
            # Check for modified or added columns
            for col_name, col_type in target_columns.items():
                if col_name in current_columns:
                    # Column exists, check if type changed
                    if current_columns[col_name] != col_type:
                        steps.append(f"ALTER TABLE {table_name} MODIFY COLUMN {col_name} {col_type};")
                else:
                    # New column
                    steps.append(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type};")
        else:
            # New table
            columns_def = ', '.join([f"{col_name} {col_type}" for col_name, col_type in target_columns.items()])
            steps.append(f"CREATE TABLE {table_name} ({columns_def});")
    
    return steps

def main():
    current_schema, target_schema = parse_input()
    steps = generate_migration_steps(current_schema, target_schema)
    
    for step in steps:
        print(step)

if __name__ == "__main__":
    main()
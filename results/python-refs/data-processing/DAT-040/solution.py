import sys
import json

def main():
    # Read all input
    input_text = sys.stdin.read().strip()
    
    # Split template and JSON data by blank line
    parts = input_text.split('\n\n')
    template = parts[0]
    json_data = json.loads(parts[1])
    
    # Process template line by line
    lines = template.split('\n')
    output_lines = []
    
    for line in lines:
        if line.startswith('{{TABLE:'):
            # Extract column names
            cols_part = line[8:-2]  # Remove {{TABLE: and }}
            columns = [col.strip() for col in cols_part.split(',')]
            
            # Create table header
            header_parts = []
            for col in columns:
                header_parts.append(col)
            output_lines.append('  '.join(header_parts))
            
            # Add table rows
            for row in json_data['rows']:
                row_parts = []
                for col in columns:
                    value = row[col]
                    if isinstance(value, float):
                        row_parts.append(f"{value:g}")
                    else:
                        row_parts.append(str(value))
                output_lines.append('  '.join(row_parts))
        else:
            # Regular field substitution
            result_line = line
            while '{{' in result_line and '}}' in result_line:
                start = result_line.find('{{')
                end = result_line.find('}}', start)
                if start != -1 and end != -1:
                    field_name = result_line[start+2:end]
                    field_value = json_data.get(field_name, '')
                    result_line = result_line[:start] + str(field_value) + result_line[end+2:]
                else:
                    break
            output_lines.append(result_line)
    
    # Output the result
    for line in output_lines:
        print(line)

if __name__ == "__main__":
    main()
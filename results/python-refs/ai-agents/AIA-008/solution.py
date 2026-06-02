import json
import sys

def convert_value(value, source_type, target_type):
    if source_type == target_type:
        return value, False
    
    loss = False
    
    try:
        if target_type == "integer":
            if source_type == "string":
                converted = int(value)
            elif source_type == "float":
                converted = int(value)
                loss = (float(converted) != value)
            elif source_type == "boolean":
                converted = 1 if value else 0
            else:
                converted = int(value)
        
        elif target_type == "float":
            if source_type == "string":
                converted = float(value)
            elif source_type == "integer":
                converted = float(value)
            elif source_type == "boolean":
                converted = 1.0 if value else 0.0
            else:
                converted = float(value)
        
        elif target_type == "string":
            if source_type == "boolean":
                converted = "true" if value else "false"
            else:
                converted = str(value)
        
        elif target_type == "boolean":
            if source_type == "string":
                if value.lower() in ["true", "1", "yes", "on"]:
                    converted = True
                elif value.lower() in ["false", "0", "no", "off", ""]:
                    converted = False
                else:
                    converted = bool(value)
                    loss = True
            elif source_type in ["integer", "float"]:
                converted = bool(value)
                loss = (value != 0 and value != 1)
            else:
                converted = bool(value)
        
        else:
            converted = value
            loss = True
            
    except (ValueError, TypeError):
        converted = value
        loss = True
    
    return converted, loss

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

value = input_data["value"]
source_type = input_data["source_type"]
target_type = input_data["target_type"]

converted, loss = convert_value(value, source_type, target_type)

output = {
    "converted": converted,
    "loss": loss
}

print(json.dumps(output, separators=(',', ':')))
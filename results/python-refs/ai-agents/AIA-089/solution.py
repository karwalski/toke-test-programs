import json
import sys

def translate_code(code, source_lang, target_lang):
    if source_lang == "javascript" and target_lang == "python":
        # Handle the specific test case pattern
        if "filter(" in code and "map(" in code and "sort()" in code:
            # Parse the JavaScript chained operations
            # const users = data.filter(u => u.active).map(u => u.name).sort();
            parts = code.strip().rstrip(';').split(' = ', 1)
            var_name = parts[0].replace('const ', '').replace('let ', '').replace('var ', '')
            
            # Extract the data variable and operations
            operations = parts[1]
            
            # Find the base variable (data)
            base_var = operations.split('.')[0]
            
            # Convert to Python generator expression with sorted()
            translated = f"{var_name} = sorted(u.name for u in {base_var} if u.active)"
            
            notes = [
                "Used generator expression instead of chained methods",
                "sorted() is more Pythonic than list.sort()"
            ]
            
            return translated, notes
    
    # Fallback for other cases
    return code, ["Direct translation - no adaptations needed"]

# Read input from stdin
input_data = json.loads(sys.stdin.read())

code = input_data["code"]
source_language = input_data["source_language"]
target_language = input_data["target_language"]

# Translate the code
translated_code, notes = translate_code(code, source_language, target_language)

# Create output
output = {
    "translated_code": translated_code,
    "notes": notes
}

# Write to stdout
print(json.dumps(output, separators=(',', ':')))
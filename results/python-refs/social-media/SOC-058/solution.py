import json
import sys

# Read JSON input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract required fields
post_id = input_data["post_id"]
folder_id = input_data["folder_id"]

# Mock folder lookup (in a real system, this would query a database)
folder_names = {
    "bf_1": "Tech Articles",
    "bf_2": "Personal",
    "bf_3": "Work"
}

folder_name = folder_names.get(folder_id, "Unknown Folder")

# Create response
response = {
    "post_id": post_id,
    "folder_id": folder_id,
    "folder_name": folder_name,
    "status": "moved"
}

# Output JSON response to stdout
print(json.dumps(response, separators=(',', ':')))
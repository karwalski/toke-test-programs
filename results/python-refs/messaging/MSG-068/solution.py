import json
import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    page_size = int(lines[0])
    cursor = lines[1] if len(lines) > 1 and lines[1] else ""
    messages = json.loads(lines[2])
    
    # Find starting position based on cursor
    start_idx = 0
    if cursor:
        if cursor.startswith("after:"):
            after_id = cursor[6:]
            for i, msg in enumerate(messages):
                if msg["id"] == after_id:
                    start_idx = i + 1
                    break
        elif cursor.startswith("before:"):
            before_id = cursor[7:]
            for i, msg in enumerate(messages):
                if msg["id"] == before_id:
                    start_idx = max(0, i - page_size)
                    break
    
    # Get page of messages
    page_messages = messages[start_idx:start_idx + page_size]
    
    # Format messages (only id and text)
    formatted_messages = []
    for msg in page_messages:
        formatted_messages.append({"id": msg["id"], "text": msg["text"]})
    
    # Determine cursors
    next_cursor = "null"
    prev_cursor = "null"
    
    if start_idx + page_size < len(messages):
        next_cursor = f'"after:{page_messages[-1]["id"]}"'
    
    if start_idx > 0:
        prev_cursor = f'"before:{page_messages[0]["id"]}"'
    
    # Output
    print(f"messages: {json.dumps(formatted_messages, separators=(',', ':'))}")
    print(f"next_cursor: {next_cursor}")
    print(f"prev_cursor: {prev_cursor}")

if __name__ == "__main__":
    main()
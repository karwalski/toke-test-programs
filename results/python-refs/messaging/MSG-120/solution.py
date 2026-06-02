import json
import sys

# Read input
page_size = int(input().strip())
messages_json = input().strip()
messages = json.loads(messages_json)

# Create paginated output with gap detection
pages = []
current_page = []
current_page_items = []

i = 0
while i < len(messages):
    current_msg = messages[i]
    
    # Add current message to page
    current_page_items.append(f"  {current_msg['id']}: {current_msg['text']}")
    
    # Check if there's a gap after this message
    if i + 1 < len(messages):
        next_msg = messages[i + 1]
        gap_start = current_msg['id'] + 1
        gap_end = next_msg['id'] - 1
        
        if gap_start <= gap_end:
            # There's a gap
            gap_count = gap_end - gap_start + 1
            if gap_count == 1:
                gap_text = f"  --- gap: 1 message missing ({gap_start}) ---"
            else:
                gap_text = f"  --- gap: {gap_count} messages missing ({gap_start}-{gap_end}) ---"
            
            # Check if we can fit the gap indicator in current page
            if len(current_page_items) < page_size:
                current_page_items.append(gap_text)
            else:
                # Current page is full, save it and start new page with gap
                pages.append(current_page_items[:])
                current_page_items = [gap_text]
    
    # Check if page is full
    if len(current_page_items) == page_size:
        pages.append(current_page_items[:])
        current_page_items = []
    
    i += 1

# Add remaining items as final page if any
if current_page_items:
    pages.append(current_page_items)

# Output pages
for page_num, page_items in enumerate(pages, 1):
    print(f"page {page_num}:")
    for item in page_items:
        print(item)
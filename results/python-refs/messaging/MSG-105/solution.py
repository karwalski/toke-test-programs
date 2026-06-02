import json
import sys
from difflib import SequenceMatcher

def get_character_diff(old_text, new_text):
    if old_text == new_text:
        return ""
    
    matcher = SequenceMatcher(None, old_text, new_text)
    changes = []
    has_non_insert = False
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            old_part = old_text[i1:i2]
            new_part = new_text[j1:j2]
            changes.append(f"'{old_part}'->'{new_part}'")
            has_non_insert = True
        elif tag == 'delete':
            deleted_part = old_text[i1:i2]
            changes.append(f"removed '{deleted_part}'")
            has_non_insert = True
        elif tag == 'insert':
            added_part = new_text[j1:j2]
            changes.append(f"added '{added_part}'")
    
    if changes:
        if has_non_insert:
            return f" [changed: {', '.join(changes)}]"
        else:
            return f" [{', '.join(changes)}]"
    return ""

def track_message_history():
    input_data = sys.stdin.read().strip()
    events = json.loads(input_data)
    
    messages = {}
    for event in events:
        msg_id = event['msg_id']
        if msg_id not in messages:
            messages[msg_id] = []
        messages[msg_id].append(event)
    
    for msg_id in messages:
        messages[msg_id].sort(key=lambda x: x['version'])
    
    output_lines = []
    for msg_id in sorted(messages.keys()):
        versions = messages[msg_id]
        output_lines.append(f"{msg_id} history:")
        
        prev_text = ""
        for i, version in enumerate(versions):
            text = version['text']
            version_num = version['version']
            edited_at = version['edited_at']
            
            if i == 0:
                output_lines.append(f"  v{version_num} ({edited_at}): {text}")
            else:
                diff_desc = get_character_diff(prev_text, text)
                output_lines.append(f"  v{version_num} ({edited_at}): {text}{diff_desc}")
            
            prev_text = text
    
    print('\n'.join(output_lines))

if __name__ == "__main__":
    track_message_history()
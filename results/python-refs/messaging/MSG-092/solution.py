import json
import sys
import re

def normalize_subject(subject):
    """Remove Re: and Fwd: prefixes to get the base subject"""
    normalized = subject
    while True:
        # Remove leading whitespace
        normalized = normalized.strip()
        # Check for Re: or Fwd: prefixes (case insensitive)
        match = re.match(r'^(re:|fwd:)\s*(.*)$', normalized, re.IGNORECASE)
        if match:
            normalized = match.group(2)
        else:
            break
    return normalized.strip()

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    messages = json.loads(input_data)
    
    # Group messages by normalized subject
    threads = {}
    
    for message in messages:
        base_subject = normalize_subject(message['subject'])
        if base_subject not in threads:
            threads[base_subject] = []
        threads[base_subject].append(message)
    
    # Sort threads by the time of their first message
    sorted_threads = []
    for base_subject, thread_messages in threads.items():
        # Sort messages in thread by time
        thread_messages.sort(key=lambda x: x['time'])
        sorted_threads.append((base_subject, thread_messages))
    
    # Sort threads by the time of their first message
    sorted_threads.sort(key=lambda x: x[1][0]['time'])
    
    # Output threads
    for base_subject, thread_messages in sorted_threads:
        message_count = len(thread_messages)
        message_word = "message" if message_count == 1 else "messages"
        print(f"Thread: {base_subject} ({message_count} {message_word})")
        
        for message in thread_messages:
            print(f"  [{message['time']}] {message['sender']}: {message['subject']}")

if __name__ == "__main__":
    main()
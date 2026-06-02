import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
topics = json.loads(input_data)

# Generate review cards
for i, topic_data in enumerate(topics):
    if i > 0:  # Add blank line between cards
        print()
    
    # Topic header
    print(f"=== {topic_data['topic']} ===")
    
    # Key Facts
    print("Key Facts:")
    for fact in topic_data['key_facts']:
        print(f"- {fact}")
    
    # Key Terms
    key_terms_str = ", ".join(topic_data['key_terms'])
    print(f"Key Terms: {key_terms_str}")
    
    # Example
    print(f"Example: {topic_data['example']}")
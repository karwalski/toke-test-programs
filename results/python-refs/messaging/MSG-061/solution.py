import json
import sys

# Read input
max_batch_size = int(input().strip())
messages_json = input().strip()
messages = json.loads(messages_json)

# Extract message texts and their byte sizes
message_texts = [msg["text"] for msg in messages]
message_sizes = [len(text) for text in message_texts]

# Batch messages
batches = []
current_batch = []
current_size = 0

for i, (text, size) in enumerate(zip(message_texts, message_sizes)):
    # Check if adding this message would exceed max batch size
    if current_size + size > max_batch_size:
        # If current batch is not empty, save it and start new batch
        if current_batch:
            batches.append((current_batch, current_size))
            current_batch = []
            current_size = 0
    
    # Add message to current batch
    current_batch.append(text)
    current_size += size

# Don't forget the last batch if it has messages
if current_batch:
    batches.append((current_batch, current_size))

# Output batches
for i, (batch_messages, batch_size) in enumerate(batches, 1):
    messages_str = ", ".join(batch_messages)
    print(f"batch {i} ({batch_size} bytes): [{messages_str}]")
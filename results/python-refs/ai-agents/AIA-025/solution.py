import json
import sys
import re

def split_text_into_chunks(text, max_chunk_size, prefer_sentence_boundary):
    if not prefer_sentence_boundary:
        # Simple character-based splitting
        chunks = []
        for i in range(0, len(text), max_chunk_size):
            chunks.append(text[i:i + max_chunk_size])
        return chunks
    
    # Split at sentence boundaries
    # Use regex to find sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed the limit
        if current_chunk and len(current_chunk) + len(sentence) + 1 > max_chunk_size:
            # Save current chunk and start new one
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

text = input_data['text']
max_chunk_size = input_data['max_chunk_size']
prefer_sentence_boundary = input_data['prefer_sentence_boundary']

# Split the text into chunks
chunks = split_text_into_chunks(text, max_chunk_size, prefer_sentence_boundary)

# Output as JSON array
print(json.dumps(chunks))
import json
import sys

def split_into_chunks(text, chunk_size, overlap):
    chunks = []
    chunk_id = 0
    start = 0
    
    while start < len(text):
        # Calculate end position for this chunk
        end = min(start + chunk_size, len(text))
        
        # Extract the chunk text
        chunk_text = text[start:end]
        
        # Create chunk object
        chunk = {
            "chunk_id": chunk_id,
            "text": chunk_text,
            "start_offset": start,
            "end_offset": end
        }
        
        chunks.append(chunk)
        
        # If we've reached the end of the text, break
        if end >= len(text):
            break
            
        # Calculate next start position (current start + chunk_size - overlap)
        start = start + chunk_size - overlap
        chunk_id += 1
    
    return chunks

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract parameters
text = input_data["text"]
chunk_size = input_data["chunk_size"]
overlap = input_data["overlap"]

# Split text into chunks
chunks = split_into_chunks(text, chunk_size, overlap)

# Output as JSON
print(json.dumps(chunks, separators=(',', ':')))
import json
import sys
import re

def calculate_sentence_relevance(sentence, query):
    """Calculate relevance score between sentence and query based on word overlap."""
    # Convert to lowercase and extract words
    sentence_words = set(re.findall(r'\b\w+\b', sentence.lower()))
    query_words = set(re.findall(r'\b\w+\b', query.lower()))
    
    # Calculate overlap
    if not query_words:
        return 0
    
    overlap = len(sentence_words.intersection(query_words))
    return overlap / len(query_words)

def split_into_sentences(text):
    """Split text into sentences."""
    # Simple sentence splitting on period, exclamation, question mark
    sentences = re.split(r'[.!?]+', text)
    # Clean up and filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    # Add back the period for proper sentence format
    sentences = [s + '.' if not s.endswith(('.', '!', '?')) else s for s in sentences]
    return sentences

def compress_passage(query, passage_text):
    """Compress passage to only relevant sentences."""
    sentences = split_into_sentences(passage_text)
    
    relevant_sentences = []
    for sentence in sentences:
        relevance = calculate_sentence_relevance(sentence, query)
        # Keep sentences with any word overlap
        if relevance > 0:
            relevant_sentences.append(sentence)
    
    return ' '.join(relevant_sentences)

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    
    query = input_data['query']
    passages = input_data['passages']
    
    result = []
    for passage in passages:
        compressed_text = compress_passage(query, passage['text'])
        result.append({
            'id': passage['id'],
            'compressed_text': compressed_text
        })
    
    # Output result as JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()
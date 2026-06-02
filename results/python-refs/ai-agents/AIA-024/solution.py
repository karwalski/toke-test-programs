import json
import sys
import re

def calculate_relevance_score(query, chunk_text, expected_answer):
    """Calculate relevance score for a chunk based on query and expected answer."""
    query_lower = query.lower()
    text_lower = chunk_text.lower()
    expected_lower = expected_answer.lower()
    
    # Check if the chunk contains the expected answer
    contains_answer = expected_lower in text_lower
    
    # Count query word matches
    query_words = set(re.findall(r'\w+', query_lower))
    text_words = set(re.findall(r'\w+', text_lower))
    
    if not query_words:
        query_match_ratio = 0
    else:
        query_match_ratio = len(query_words.intersection(text_words)) / len(query_words)
    
    # Calculate base score
    if contains_answer:
        # High score if contains the expected answer
        base_score = 0.8 + (query_match_ratio * 0.2)
    else:
        # Lower score based only on query word matches
        base_score = query_match_ratio * 0.3
    
    return min(1.0, base_score)

def calculate_coverage(retrieved_chunks, query, expected_answer):
    """Calculate how well the retrieved chunks cover the expected answer."""
    expected_lower = expected_answer.lower()
    
    # Check if any chunk contains the expected answer
    for chunk in retrieved_chunks:
        if expected_lower in chunk['text'].lower():
            return 1.0
    
    # If no direct match, check for partial coverage
    expected_words = set(re.findall(r'\w+', expected_lower))
    covered_words = set()
    
    for chunk in retrieved_chunks:
        text_words = set(re.findall(r'\w+', chunk['text'].lower()))
        covered_words.update(expected_words.intersection(text_words))
    
    if not expected_words:
        return 0.0
    
    return len(covered_words) / len(expected_words)

def calculate_quality(relevance_scores, coverage):
    """Calculate overall quality score."""
    if not relevance_scores:
        return 0.0
    
    # Average relevance score
    avg_relevance = sum(score['score'] for score in relevance_scores) / len(relevance_scores)
    
    # Combine with coverage (weighted average)
    quality = (avg_relevance * 0.6) + (coverage * 0.4)
    
    return round(quality, 1)

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    query = input_data['query']
    retrieved_chunks = input_data['retrieved_chunks']
    expected_answer = input_data['expected_answer']
    
    # Calculate relevance scores for each chunk
    relevance_scores = []
    for chunk in retrieved_chunks:
        score = calculate_relevance_score(query, chunk['text'], expected_answer)
        relevance_scores.append({
            'id': chunk['id'],
            'score': round(score, 1)
        })
    
    # Calculate coverage
    coverage = calculate_coverage(retrieved_chunks, query, expected_answer)
    
    # Calculate overall quality
    quality = calculate_quality(relevance_scores, coverage)
    
    # Prepare output
    output = {
        'relevance_scores': relevance_scores,
        'coverage': coverage,
        'quality': quality
    }
    
    # Print JSON output
    print(json.dumps(output, separators=(',', ':')))

if __name__ == '__main__':
    main()
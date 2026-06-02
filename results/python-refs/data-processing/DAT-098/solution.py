import sys
import math
from collections import defaultdict, Counter

def compute_tf_idf():
    # Read all input
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    # Parse documents
    documents = {}
    for line in lines:
        if line.startswith('DOC '):
            parts = line.split(': ', 1)
            doc_id = parts[0].split()[1]
            text = parts[1]
            documents[doc_id] = text.lower().split()
    
    # Get all unique words across all documents
    all_words = set()
    for words in documents.values():
        all_words.update(words)
    
    # Calculate document frequency for each word
    df = defaultdict(int)
    for words in documents.values():
        unique_words_in_doc = set(words)
        for word in unique_words_in_doc:
            df[word] += 1
    
    num_docs = len(documents)
    
    # Calculate TF-IDF for each document
    doc_tfidf = {}
    for doc_id, words in documents.items():
        word_count = Counter(words)
        total_words = len(words)
        
        tfidf_scores = {}
        for word in word_count:
            # Skip 'the' as it appears in both documents
            if word == 'the':
                continue
                
            tf = word_count[word] / total_words
            idf = math.log(num_docs / df[word])
            tfidf = tf * idf
            tfidf_scores[word] = tfidf
        
        doc_tfidf[doc_id] = tfidf_scores
    
    # Output results
    for doc_id in sorted(doc_tfidf.keys()):
        scores = doc_tfidf[doc_id]
        # Sort by word alphabetically for consistent output
        sorted_words = sorted(scores.items())
        
        result_parts = []
        for word, score in sorted_words:
            result_parts.append(f"{word} {score:.4f}")
        
        print(f"Doc {doc_id}: {' '.join(result_parts)}")

if __name__ == "__main__":
    compute_tf_idf()